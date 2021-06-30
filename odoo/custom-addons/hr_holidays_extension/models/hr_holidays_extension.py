
from odoo import api, fields, models, tools, _
from odoo.osv import expression
class HolidaysRequest(models.Model):
    _inherit = 'hr.leave'

    @api.model
    def action_by_employee(self):

        domain = []
        # if not manager = normal user 
        if not self.user_has_groups('hr_holidays.group_hr_holidays_responsible'):
            domain = expression.AND([
                domain,
                [('employee_id.user_id', '=', self._uid)]
            ])
        # if not admin but manager ( as it pass the first condition )
        elif not self.user_has_groups('hr_holidays.group_hr_holidays_manager'):
            domain = expression.AND([
                domain,
                ['|',('employee_id.parent_id.user_id', '=', self._uid),('employee_id.user_id', '=', self._uid)]
            ])
        # else Hr or Admin no restriction
        else:
            pass

        return {
            'name': _('Time Off Analysis'),
            'type': 'ir.actions.act_window',
            'res_model': 'hr.leave',
            'view_mode': 'graph,pivot,calendar,form',
            'search_view_id': self.env.ref('hr_holidays_extension.view_hr_by_employee_holidays_filter_report').id,
            'domain': domain,
            'context': {'search_default_year': 1, 
            'search_default_group_employee': 1, 
            'search_default_group_type': 1}
        }