
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from lxml import etree
import json
class ProjectTaskType(models.Model):
    _inherit = 'project.task'

class Project(models.Model):
    _inherit = "project.project"
    
    department_primary_id = fields.Many2one(
        'hr.department', string='Principal Department', required=True)

    department_secondary_id = fields.Many2many("hr.department", "project_department_rel", "project_id", "department_id", string="Secondary Departments")

    user_id = fields.Many2one('res.users', string='Project Manager', default=None, tracking=True)

    project_planned_duration = fields.Float("Project Duration", help="Estimation duration of the project (per days)")

    isResponsible = fields.Boolean('isResponsible', compute='_check_is_responsible')

    @api.depends('user_id')
    def _check_is_responsible(self):
        for project in self:
            project.isResponsible = False
            if self.user_has_groups('project_extension.group_project_responsible') and not self.user_has_groups('project.group_project_manager'):
                project.isResponsible = True

    @api.model
    def default_get(self, fields_list):
        result = super().default_get(fields_list)
        # we need to get the department for this user
        employees = self.env['hr.employee'].search([('user_id' ,'=' ,self.env.user.id)])
        if employees.department_id:
            result['department_primary_id'] = employees.department_id
            result['user_id'] = self.env.user
        else:
            result.pop('user_id')

        return result

    #user_id = fields.Many2one('res.users', string='Project Manager', default=lambda self: self.env.user, tracking=True)
    @api.onchange('department_primary_id')
    def _get_user_by_department(self):
        res={"domain":{'user_id':[('id','in', []),]}}
        # A manager cannot choose another project manager
        # it will be set by default
        for prj in self:
            if prj.department_primary_id:
                employees = self.env['hr.employee'].search([('department_id' ,'=' ,prj.department_primary_id.id)])
                # we keep the user selected in case it belongs to the department
                if prj.user_id not in employees.mapped('user_id'):
                    prj.user_id = False
                res['domain']={'user_id':[('id','in', employees.mapped('user_id').ids),]}
            else:
                res['domain']={'user_id':[('id','in', []),]}
        return res

    @api.model
    def open_create_project(self):
        # Display differenrt view based on the user group
        view_ID = self.env.ref('project_extension.project_project_view_extension_hr_responsible_form_simplified').id
        if self.user_has_groups('project.group_project_manager'):
            view_ID = self.env.ref('project_extension.project_project_view_extension_hr_manager_form_simplified').id

        return {
            'name': _('Create Project'),
            'type': 'ir.actions.act_window',
            'res_model': 'project.project',
            'view_mode': 'form',
            'view_id': view_ID,
            'target':'new'
        }

class Task(models.Model):
    _inherit = "project.task"
        
    @api.model
    def _set_user_domain(self):
        res = [('share', '=', False)]
        # i am manager
        if  self.user_has_groups('project_extension.group_project_responsible') and not self.user_has_groups('project.group_project_manager'):
            # get the employees managed
            employees = self.env['hr.employee'].search([('parent_id.user_id' ,'=' ,self.env.user.id)])
            # if employees found add them otherwise i can assign task to me only
            if employees:
                res = ['&',('share', '=', False),'|',('id','in',employees.mapped('user_id').ids),('id','=',self.env.user.id)]
            else:
                res = [('id','=',self.env.user.id)]
        return res

    user_id = fields.Many2one('res.users',
        string='Assigned to',
        default=None,
        index=True, tracking=True,
        domain=lambda self: self._set_user_domain()
        )

    def write(self, vals):
        # workarround with kanban view
        # issue : tasks sequence are updated
        if (vals.get('sequence', False) or  str(vals.get('sequence', False)) == '0') and len(vals) == 1:
            return True
        return super().write(vals)

    @api.model
    def fields_view_get(self, view_id, view_type, toolbar = False, submenu= False):
        result = super().fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        if view_type == "form":
            doc = etree.XML(result['arch'])
            # we get the fild using xpath search
            # we can also add domain function in the project attribute definition
            project_id_field = doc.xpath("//group/group/field[@name='project_id']")
            if project_id_field:
                # normal user cannot change the project it belongs to
                if  not self.user_has_groups('project_extension.group_project_responsible'):
                    self.applyModifier(project_id_field[0],"readonly",True)

                # manager domain update
                if  self.user_has_groups('project_extension.group_project_responsible') and not self.user_has_groups('project.group_project_manager'):
                    domain = project_id_field[0].get('domain','[]')[:-1] + ", ('user_id', '=', uid)]"
                    project_id_field[0].set('domain', domain)

            user_id_field = doc.xpath("//group/group/field[@name='user_id']")

            if user_id_field:
                # normal user cannot assaign task to another 
                if  not self.user_has_groups('project_extension.group_project_responsible'):
                    self.applyModifier(user_id_field[0],"readonly",True)
                    
            result['arch'] = etree.tostring(doc, encoding="unicode")

        return result


    def applyModifier(self, node, modifierAttribute, value = True):
        node.set(modifierAttribute, '1' if True else '0')
        modifier = json.loads(node.get("modifiers"))
        modifier[modifierAttribute] = value
        node.set("modifiers", json.dumps(modifier))
