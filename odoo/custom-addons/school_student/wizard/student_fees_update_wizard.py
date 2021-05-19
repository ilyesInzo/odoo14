from odoo import api, models, fields

class StudentFeesUpdateWizard(models.TransientModel):
    _name="student.fees.update.wizard"
    total_fees = fields.Float(string="Fees")


    # there are 4 ways to open wizard button
    # 1- adding button type obect in the parent view exp school_student and open the wizard from the method called
    # 2- adding button but type action
    # 3- adding to the Action menu (where we have duplicate/archive...)
    # 4- adding in the menu directly like hobby
    def update_fees(self):

        # we have to access the student model and change its value
        self.env['school.student'].browse(self._context.get("active_ids")).update({'student_fees':self.total_fees})

        return True

# we can also inherit wizard
class StudentFeesExtendUpdateWizard(models.TransientModel):
    _inherit="student.fees.update.wizard"
    parent_name = fields.Char(string="Parent Name")