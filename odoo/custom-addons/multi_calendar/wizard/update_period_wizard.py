# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import datetime

class UpdatePeriod(models.TransientModel):
    _name = 'update.period.wizard'

    start_time = fields.Date(string="Start Time", default=datetime.today())
    end_time = fields.Date(string="End Time")
    calendar_id = fields.Many2one('calendar.calendar', string="Calendar")

    def update_dates(self):
        
        active_ids = self.env.context.get('active_ids')
        for rec in self:
            if active_ids:
                selected_employees = self.env['calendar.assignee'].browse(active_ids)
                selected_employees.write({            
                'start_time': rec.start_time,
                'end_time': rec.end_time
                })
        return True

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
        
