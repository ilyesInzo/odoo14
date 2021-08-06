# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime


class Meeting(models.Model):
    _inherit = 'calendar.event'

    calendar_id = fields.Many2one('calendar.calendar',
                                  string='Calendar',
                                  readonly=False,
                                  index=True,
                                  tracking=True,
                                  check_company=True,
                                  change_default=True)


class Calendar(models.Model):
    _name = 'calendar.calendar'

    @api.model
    def _set_calendar_domain(self):
        # As a calendar can only have one sub_child
        return [('child_ids', '=', False)]

    name = fields.Char('Name')
    is_default = fields.Boolean('Default')

    event_ids = fields.One2many('calendar.event',
                                'calendar_id',
                                string='Events')
    time_ids = fields.One2many('calendar.time', 'calendar_id', string="Time")
    assignee_ids = fields.One2many('calendar.assignee',
                                   'calendar_id',
                                   string="Assignee")
    child_ids = fields.One2many('calendar.calendar',
                                'parent_id',
                                string='Child Calendars')

    parent_id = fields.Many2one(
        'calendar.calendar',
        string='Parent Calendar',
        domain=lambda self: self._set_calendar_domain())

    start_time = fields.Date(string="Start Time", default=datetime.today())
    end_time = fields.Date(string="End Time")
    description = fields.Html()

    sub_calendar = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
    ],
                                    string="Sub-calendar",
                                    default="yes")

    @api.onchange('is_default')
    def _compute_is_default(self):
        for calendar in self:
            if calendar.is_default:
                return {
                    'warning': {'title': "Warning", 
                    'message': "Employees having regular work times will be assigned automatically to that new calendar."},
                }       

    @api.onchange('sub_calendar')
    def _compute_sub_calendar(self):
        for calendar in self:
            if calendar.sub_calendar == 'no':
                calendar.parent_id = None
                calendar.start_time = None
                calendar.end_time = None
                return {
                    'warning': {'title': "Warning", 
                    'message': "Employees will be re-assigned to related main calendar"},
                } 

    @api.onchange('parent_id', 'start_time', 'end_time')
    def _compute_date(self):
        for calendar in self:

            if calendar.parent_id:
                print(calendar.parent_id.start_time)
                if calendar.start_time and calendar.start_time < calendar.parent_id.start_time:
                    calendar.start_time = calendar.parent_id.start_time

                if calendar.end_time and calendar.parent_id.end_time and calendar.end_time > calendar.parent_id.end_time:
                    calendar.end_time = calendar.parent_id.end_time

            if calendar.start_time and calendar.end_time and calendar.start_time > calendar.end_time:
                calendar.end_time = calendar.start_time

    @api.constrains('is_default')
    def _check_is_default(self):
        if self.is_default:
            calendars = self.env['calendar.calendar'].search([('id', '!=',
                                                               self.id)])
            for calendar in calendars:
                calendar.is_default = False

    @api.constrains('parent_id')
    def _check_parent_id(self):
        if not self._check_recursion():
            raise ValidationError(_('You cannot create recursive calendars.'))

    # avoid employee redundancy & date range check
    @api.constrains('assignee_ids')
    def _check_exist_assigned_employee(self):
        # employee id
        assignee_ids = []
        for calendar in self:
            for assignee in calendar.assignee_ids:

                if assignee.start_time and assignee.start_time < calendar.start_time:
                    raise ValidationError(
                        _("Employee's start date assignment should be >= to calendar start date."
                          ))

                if assignee.end_time and calendar.end_time and assignee.end_time > calendar.end_time:
                    raise ValidationError(
                        _("Employee's end date assignment should be <= to calendar start end."
                          ))

                if assignee.employee_id.id in assignee_ids:
                    raise ValidationError(_('Employee already added.'))
                assignee_ids.append(assignee.employee_id.id)
        return True

    @api.model
    def default_get(self, fields_list):

        result = super().default_get(fields_list)
        vals = [(0, 0, {
            'day': 'monday',
            'work_Time': 8
        }), (0, 0, {
            'day': 'tuesday',
            'work_Time': 8
        }), (0, 0, {
            'day': 'wednesday',
            'work_Time': 8
        }), (0, 0, {
            'day': 'thursday',
            'work_Time': 8
        }), (0, 0, {
            'day': 'friday',
            'work_Time': 8
        }), (0, 0, {
            'day': 'saturday',
            'work_Time': 0
        }), (0, 0, {
            'day': 'sunday',
            'work_Time': 0
        })]

        result.update({'time_ids': vals})

        return result

    @api.model
    def create(self, vals_list):
        # as all employee are assigned to the default we don't choose one
        if vals_list.get('is_default', False):
            vals_list['assignee_ids'] = []

        return super().create(vals_list)

    def write(self, vals):
        # if the default is true we have to remove all assignee from db

        result = super().write(vals)
        # must be added after the write

        # We must have exactly one default
        # if a record turn to true the other turn to false : this is done by the constraint
        # but if a record turn to false? we raise a validation error (check existing record in db)

        # Attention, this doesn't mean that the current record is turned to false
        # the constraint will update all the other records also in case this one turn to true

        if vals.get('is_default', None) is False:
            default_calender_id = self.env['calendar.calendar'].search(
                [('is_default', '=', 'True')], limit=1)
            if not default_calender_id:
                raise ValidationError(
                    _('We must have at least one default calendar!'))
        # the case the calendar turn to default, all employee are assigned so we remove the assignee list
        # to not enter this condition in case is_default not provided we use elif unstead of else
        elif vals.get('is_default', None) is True:
            default_calender_id = self.env['calendar.calendar'].search(
                [('is_default', '=', 'True')], limit=1)
            assigned_employees = self.env['calendar.assignee'].search([
                ('calendar_id', '=', default_calender_id.id)
            ])

            if assigned_employees:
                assigned_employees.unlink()
        return result

    def unlink(self):

        for project in self:
            if not project.is_default:
                return super().unlink()
            else:
                raise ValidationError(
                    _('You are not allowed to delete the default calendar'))
        return False

    # called during installation only to bind records
    @api.model
    def action_init_data(self):
        # we should get the record created from data
        default_calender_id = self.env['calendar.calendar'].search(
            [('is_default', '=', 'True')], limit=1)
        # all the already created event should be with empty calendar_id
        calendar_events = self.env['calendar.event'].search([('calendar_id',
                                                              '=', None)])
        if calendar_events:
            calendar_events.write({'calendar_id': default_calender_id})

    def action_view_calendar(self):
        action = self.env.ref('calendar.action_calendar_event').read()[0]
        domain = [('calendar_id', 'in', self.ids)]
        action.update({"domain": domain})
        return action


class CalendarTime(models.Model):
    _name = "calendar.time"

    calendar_id = fields.Many2one('calendar.calendar',
                                  string="Calendar",
                                  ondelete='cascade')
    day = fields.Selection([('monday', 'Monday'), ('tuesday', 'Tuesday'),
                            ('wednesday', 'Wednesday'),
                            ('thursday', 'Thursday'), ('friday', 'Friday'),
                            ('saturday', 'Saturday'), ('sunday', 'Sunday')],
                           string="Day")

    work_Time = fields.Float(string="Work Time")

    @api.model
    def default_get(self, fields_list):

        rel = super().default_get(fields_list)
        return rel


class CalendarAssignee(models.Model):
    _name = "calendar.assignee"

    @api.model
    def _set_calendar_domain(self):

        return [('is_default', '=', 'False')]

    @api.model
    def _set_empoyee_domain(self):

        # Once the employee assigned to a calendar, we will not add it to list (even if the sql constraint can double check )
        employee_ids = self.env['calendar.assignee'].search([])
        if employee_ids:
            return [('id', 'not in', employee_ids.mapped('employee_id').ids)]
        else:
            return []

    _rec_name = "employee_id"
    calendar_id = fields.Many2one('calendar.calendar',
                                  string="Calendar",
                                  ondelete='cascade')
    employee_id = fields.Many2one(
        'hr.employee')  # , domain=lambda self: self._set_empoyee_domain()

    start_time = fields.Date(string="Start Time", default=datetime.today())
    end_time = fields.Date(string="End Time")

    @api.onchange('start_time', 'end_time')
    def _compute_date(self):
        for assignee in self:

            if assignee.calendar_id:
                if assignee.start_time and assignee.start_time < assignee.calendar_id.start_time:
                    assignee.start_time = assignee.calendar_id.start_time
                    #raise ValidationError(_("Employee's start date assignment should be >= to calendar start date."))

                if assignee.end_time and assignee.calendar_id.end_time and assignee.end_time > assignee.calendar_id.end_time:
                    assignee.end_time = assignee.calendar_id.end_time
                    #raise ValidationError(_("Employee's end date assignment should be <= to calendar start end."))

            if assignee.start_time and assignee.end_time and assignee.start_time > assignee.end_time:
                assignee.end_time = assignee.start_time

    @api.onchange('employee_id')
    def _get_user_by_department(self):
        res = {}
        # A manager cannot choose another project manager
        # it will be set by default
        employee_ids = self.env['calendar.assignee'].search([])
        if employee_ids:
            res = {
                "domain": {
                    'employee_id':
                    [('id', 'not in', employee_ids.mapped('employee_id').ids)]
                }
            }
        return res

    def open_update_dates(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": "update.period.wizard",
            "view_mode": "form",
            "target": "new",
            'context': self.env.context
        }

    @api.model
    def create(self, vals_list):

        return super().create(vals_list)

    _sql_constraints = [('unique_employee', 'UNIQUE (employee_id)',
                         'You can not affect an employee twice')]
