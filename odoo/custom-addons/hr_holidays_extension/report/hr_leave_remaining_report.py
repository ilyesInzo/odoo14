# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools, exceptions, _
from odoo.osv import expression


class LeaveRemainingReport(models.Model):
    _name = "hr.leave.remaining.report"
    _description = 'Remaining Leaves Report'
    _auto = False
    _order = "date_from DESC, employee_id"

    employee_id = fields.Many2one('hr.employee', string="Employee", readonly=True)
    name = fields.Char('Description Remaining', readonly=True)
    #number_of_days = fields.Float('Number of Days', readonly=True)
    #consumed_leave = fields.Float( string='Consumed Days', readonly=True)
    remaining_leave = fields.Float( string='Remaining Days', readonly=True)
    department_id = fields.Many2one('hr.department', string='Department', readonly=True)
    category_id = fields.Many2one('hr.employee.category', string='Employee Tag', readonly=True)
    holiday_status_id = fields.Many2one("hr.leave.type", string="Leave Type", readonly=True)
    state = fields.Selection([
        ('draft', 'To Submit'),
        ('cancel', 'Cancelled'),
        ('confirm', 'To Approve'),
        ('refuse', 'Refused'),
        ('validate1', 'Second Approval'),
        ('validate', 'Approved')
        ], string='Status', readonly=True)
    holiday_type = fields.Selection([
        ('employee', 'By Employee'),
        ('category', 'By Employee Tag')
    ], string='Allocation Mode', readonly=True)
    date_from = fields.Datetime('Start Date', readonly=True)
    date_to = fields.Datetime('End Date', readonly=True)
    payslip_status = fields.Boolean('Reported in last payslips', readonly=True)


    def _calculate(self):
        print("vavla")
        for leave in self:
            leave.remaining_days = 2

    def init(self):
        tools.drop_view_if_exists(self._cr, 'hr_leave_remaining_report')
        self._cr.execute("""
            CREATE or REPLACE view hr_leave_remaining_report as (
                SELECT row_number() over(ORDER BY leaves.employee_id) as id,
                leaves.employee_id as employee_id, leaves.name as name,
                leaves.number_of_days as number_of_days, leaves.consumed_leave as consumed_leave,
				(leaves.number_of_days - leaves.consumed_leave) as remaining_leave,
                leaves.category_id as category_id, leaves.department_id as department_id,
                leaves.holiday_status_id as holiday_status_id, leaves.state as state,
                leaves.holiday_type as holiday_type, leaves.date_from as date_from,
                leaves.date_to as date_to, leaves.payslip_status as payslip_status
				
                from (select
                    allocation.employee_id as employee_id,
                    allocation.private_name as name,
                    allocation.number_of_days as number_of_days,
                    allocation.category_id as category_id,
                    allocation.department_id as department_id,
                    allocation.holiday_status_id as holiday_status_id,
                    allocation.state as state,
                    allocation.holiday_type,
                    null as date_from,
                    null as date_to,
                    FALSE as payslip_status,
					(select
                       COALESCE(sum(request.number_of_days),0) as number_of_days
                from hr_leave as request
					where request.employee_id = allocation.employee_id and request.holiday_status_id = allocation.holiday_status_id
					) as consumed_leave
					  
                from hr_leave_allocation as allocation ) leaves
            );
        """)

    @api.model
    def action_remaining_report(self):
        print('My BABYYYYYYY ------------------***********-----------')
        
        domain = [('holiday_type', '=', 'employee'),('employee_id.user_id', '=', self._uid)]

        if self.env.context.get('active_ids'):
            domain = expression.AND([
                domain,
                [('employee_id', 'in', self.env.context.get('active_ids', []))]
            ])
        return {
            'name': _('Remaining Analysis'),
            'type': 'ir.actions.act_window',
            'res_model': 'hr.leave.remaining.report',
            'view_mode': 'graph,tree,form',
            'search_view_id': self.env.ref('hr_holidays.view_hr_holidays_filter_report').id,
            'domain': domain,
            'context': {
                'search_default_group_employee': True,
                'search_default_group_type': True,
                'search_default_year': True,
                'search_default_validated': True,
            }
        }

    @api.model
    def action_employee_remaining_report(self):
        print('My BABYYYYYYY ------------------***********-----------')


        # do not display my one report
        domain = [('holiday_type', '=', 'employee'),('employee_id.user_id', '!=', self._uid)]
        # if not has hr (so not admin also) and has manager display my team report


        if not self.user_has_groups('hr_holidays.group_hr_holidays_manager') and self.user_has_groups('hr_holidays.group_hr_holidays_responsible'):
            domain = expression.AND([
                domain,
                [('employee_id.parent_id.user_id', '=', self._uid)]
            ])

        if self.env.context.get('active_ids'):
            domain = expression.AND([
                domain,
                [('employee_id', 'in', self.env.context.get('active_ids', []))]
            ])
        return {
            'name': _('Employee Remaining Analysis'),
            'type': 'ir.actions.act_window',
            'res_model': 'hr.leave.remaining.report',
            'view_mode': 'graph,tree,form',
            'search_view_id': self.env.ref('hr_holidays_extension.view_hr_holidays_remaining_leave_filter_report').id,
            'domain': domain,
            'context': {
                'search_default_group_employee': True,
                'search_default_group_type': True,
                'search_default_year': True,
                'search_default_validated': True,
            }
        }

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):

        

        if not self.user_has_groups('hr_holidays.group_hr_holidays_user') and 'name' in groupby:
            raise exceptions.UserError(_('Such grouping is not allowed.'))
        return super(LeaveRemainingReport, self).read_group(domain, fields, groupby, offset=offset, limit=limit, orderby=orderby, lazy=lazy)


