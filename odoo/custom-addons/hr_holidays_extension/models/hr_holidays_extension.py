
from odoo import api, fields, models, tools

class HolidaysRequest(models.Model):
    _inherit = 'hr.leave'

    # adding bu me start
    number_of_Remaining_days = fields.Float(string="Remaining Days", compute='_compute_number_of_Remaining_days', store=True, default=5)
    # adding bu me end


    # add new Start
    def _compute_number_of_Remaining_days(self):
        print('Laslousa')
        for holiday in self:
            print(holiday.number_of_days)
            holiday.number_of_Remaining_days = 5
    # add new End