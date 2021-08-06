# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import datetime

class AssignEmployees(models.TransientModel):
    _name = 'assigne.employees.wizard'

    employee_ids = fields.Many2many(
        'hr.employee',string="Employees")
    start_time = fields.Date(string="Start Time", default=datetime.today())
    end_time = fields.Date(string="End Time")
    calendar_id = fields.Many2one('calendar.calendar', string="Calendar")

    @api.onchange('employee_ids', 'calendar_id')
    def _get_user_by_department(self):
        res={}
        # A manager cannot choose another project manager
        # it will be set by default
        employee_ids = self.env['calendar.assignee'].search([])
        if employee_ids:
            res =  {"domain":{'employee_ids':[('id', 'not in', employee_ids.mapped('employee_id').ids)]}}  
        return res

    def action_assigne_employees(self):
        vals = []
        for rec in self:
            for employee in rec.employee_ids:
                vals.append({
            'start_time': rec.start_time,
            'end_time': rec.end_time,
            'calendar_id': self.calendar_id.id,
            'employee_id': employee.id,
        })
        if vals:
            self.env['calendar.assignee'].create(vals)

        return {
            'type': 'ir.actions.client',
            'tag': 'reload',  } 


    @api.onchange('start_time', 'end_time')
    def _compute_date(self):
        for assignee in self:

            if assignee.calendar_id:
                if assignee.start_time and  assignee.start_time < assignee.calendar_id.start_time:
                   assignee.start_time = assignee.calendar_id.start_time
                    #raise ValidationError(_("Employee's start date assignment should be >= to calendar start date."))

                if assignee.end_time and assignee.calendar_id.end_time and  assignee.end_time > assignee.calendar_id.end_time:
                   assignee.end_time = assignee.calendar_id.end_time
                    #raise ValidationError(_("Employee's end date assignment should be <= to calendar start end."))

            if assignee.start_time and assignee.end_time and assignee.start_time > assignee.end_time:
               assignee.end_time = assignee.start_time
        
