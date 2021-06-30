# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class Project(models.Model):
    _inherit = "project.project"

    # use_template = fields.Boolean(string="Use Template", store = False)
    # if the project is created from template avoid changing the template
    created_from_template = fields.Boolean('created from template', default = False)
    project_template_id = fields.Many2one('project.project.template', string='Project Template')

    @api.model
    def create(self, vals):
        if  vals.get('project_template_id', False): 
            vals = self._create_Task_From_Template(vals)
        return super(Project, self).create(vals)
   
    @api.model
    def write(self, vals):
        #or project in self:
            # if the project is already created from template avoid re-creating the tasks
            
            # we will allow changing template
            # if not project.created_from_template :
            # if the project_template is False this mean it was removed (not required field)
        if  vals.get('project_template_id', None) is not None:
            # we will remove all existing tasks
            for project in self:
                self.env["project.task"].search([('id','in',project.task_ids.ids)]).unlink()
            if vals.get('project_template_id', False):
                vals = self._create_Task_From_Template(vals)

        print(vals)
        return super(Project, self).write(vals)


    def _create_Task_From_Template(self, vals):

            # no value present we have to send request
            # self.mapped('project_template_id').task_ids
            project_tasks = vals.get('task_ids', [])
            tempalte_tasks = self.env['project.task.template'].search([('project_template_id','=',vals.get('project_template_id'))])
            vals['created_from_template'] = True
            for task in tempalte_tasks:
               project_tasks.append([0, False, {'name': task.name, 'user_id': None}])
            vals['task_ids'] = project_tasks
            return vals

    def action_create_template(self):
        
        action = self.env['ir.actions.act_window']._for_xml_id("project_template.project_create_portal")
        for project in self:
            template_tasks = [ [0, False, {'name': task.name}] for task in project.task_ids]
            action['context']= {'default_name': project.name , 'default_task_ids': template_tasks}
        return action


class Task(models.Model):
    _inherit = "project.task"


class project_template(models.Model):
    _name = 'project.project.template'
    _description = 'Create project templates used later to inti a new created project'

    name = fields.Char(string='Project', required=True)
    description = fields.Html()
    task_ids = fields.One2many('project.task.template', 'project_template_id', string='Tasks')

    @api.model
    def create(self, vals_list):
        self._check_task_existance(vals_list.get('task_ids', []))
        return super(project_template, self).create(vals_list)
        
    def write(self, vals):
        # this must be called here, because e need the final result 
        # otherwise the self.task_ids will not have the current states (the removed tasks will be showen also)
        result = super().write(vals)
        self._check_task_existance(self.task_ids)
        return result

    # at least one task template must be provided
    def _check_task_existance(self, tempalte_tasks):
        if not tempalte_tasks:
            raise UserError(_("Please add at least one task."))

class task_template(models.Model):
    _name = 'project.task.template'
    _description = 'Tasks belongs to the project template'

    name = fields.Char(string='Task', required=True)
    project_template_id = fields.Many2one('project.project.template', string='Project Template',readonly=False,
        index=True, tracking=True, check_company=True, change_default=True)
    description = fields.Html(string='Description')
