# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools, exceptions, _
from odoo.osv import expression


class LeaveReport(models.Model):
    _inherit ="hr.leave.report"

    # check user authorization and change display based on them
    @api.model
    def action_time_off_analysis(self):
        result = super(LeaveReport, self).action_time_off_analysis()
        domain = result.get('domain')

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
        result['domain'] = domain
        return result

  