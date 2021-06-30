
from odoo import api, fields, models

class HolidaysType(models.Model):
    _inherit = "hr.leave.type"

    # to add condition and display fewer time off type report in the dashboard

    """@api.model
    def get_days_all_request(self):

        leave_types = sorted(self.search([]).filtered(lambda x: x.name != 'Test Leave 1' and ( x.virtual_remaining_leaves or x.max_leaves) ), key=self._model_sorting_key, reverse=True)
        
        return [(lt.name, {
                    'remaining_leaves': ('%.2f' % lt.remaining_leaves).rstrip('0').rstrip('.'),
                    'virtual_remaining_leaves': ('%.2f' % lt.virtual_remaining_leaves).rstrip('0').rstrip('.'),
                    'max_leaves': ('%.2f' % lt.max_leaves).rstrip('0').rstrip('.'),
                    'leaves_taken': ('%.2f' % lt.leaves_taken).rstrip('0').rstrip('.'),
                    'virtual_leaves_taken': ('%.2f' % lt.virtual_leaves_taken).rstrip('0').rstrip('.'),
                    'request_unit': lt.request_unit,
                }, lt.allocation_type, lt.validity_stop)
            for lt in leave_types]
"""
