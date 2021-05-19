
from odoo import api, models, fields

# we commonly keep the same class name
class school_student(models.Model):
    _inherit = "school.student"

    student_full_name = fields.Char(string="Full Name")