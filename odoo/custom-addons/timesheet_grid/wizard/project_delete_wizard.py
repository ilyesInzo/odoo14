# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ProjectDelete(models.TransientModel):
    _inherit = 'project.delete.wizard'
    _description = 'Project Delete Wizard'

    def action_archive(self):
        print('******* Archive Projects ********')
        print(self.project_ids)
        self.project_ids.write({'active': False})

    def confirm_delete(self):
        print('******* Delete Projects ********')
        self.with_context(active_test=False).project_ids.unlink()
        return self.env["ir.actions.actions"]._for_xml_id("project.open_view_project_all_config")
