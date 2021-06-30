# -*- coding: utf-8 -*-

from collections import namedtuple
from odoo import models, fields, api, _, registry, tools
from odoo.exceptions import UserError
from lxml import etree
import datetime

# second inheritance type is to inherit all fields in the student 
# in addition the address class must be declared before the classes using it in the same file
class Address(models.Model):
    _name = "address"
    street = fields.Char(string="Street")
    street_one = fields.Char(string="Street2")
    city = fields.Char(string="City")
    state = fields.Char(string="State")
    country = fields.Char(string="Country")
    zip_code = fields.Char(string="Zip code")

class school_student(models.Model):
    _name = 'school.student'
    _inherit = "address"
    _description = 'school_student' # what is the model used for

    #other attributes :
    # _auto = True # automatically create the table related to this model
    # _sql_constraints = [('constrName','constrCondition','UserMessage')] table level constraint 
    # _sequence to use custom sequence name for the id field
    # _transient = True to create transient model (if the model inherit models.Transiant this field is set to true automatically) 
    # _abstract create abstract model by default is False
    # _fold_name used to group in kanban view
    # _parent_name = "Many2One child name in same model"
    # _parent_store = True an additional field Parant_Path should be added
    # _log_access = True when create/update the createby/writeBy audit will be added otherwise no


    # _table = 'TableName' # to have different table name in psgr instead of using the _name as table name
    # but Attention when using the self.env we give always the _name as param
    name = fields.Char()
    # we have to create the ref key and give the _name module of the related class
    school_id = fields.Many2one("school.profile", string="School")
    # 4 mondatory params : related model, relational TableName, id of the current table, id of the relatedModelTable
    hobby_list = fields.Many2many(
        "hobby", "school_hobby_rel", "student_id", "hobby_id", string="Hobbies")
    # make adding/selecting/cheking one value mondatory as required=True don't apply for many2many

    # we will make a related dataType (e.g. displaying some school information in student not only the school name which is showen by default)
    # the_related_foreign_key.the_real_field
    # store=True (this will make this field saved)
    is_virtual = fields.Boolean(related="school_id.is_virtual_school")
    school_adress = fields.Text(related="school_id.address")

    # monatry attribute
    # to achieve that we need two attribute the currency and the monetry
    # res.currency is an odoo module
    currency_id = fields.Many2one("res.currency", string="currency")
    student_fees = fields.Monetary(string="Student fees")

    bDate = fields.Date(string="Birth Date")

    student_age = fields.Char(string="Total Age", compute="_get_age_from_student", readonly=True)

    # with this decorator the change will operate dynamically when the bDate changes
    # otherwise the value will change after save
    @api.depends("bDate")
    def _get_age_from_student(self):
        today_date = datetime.date.today()
        for stud in self:
            if stud.bDate:
                birthDate = fields.Datetime.to_datetime(stud.bDate).date()
                self.student_age = str(int((today_date - birthDate).days / 365))
            else:
                self.student_age = "No Calculation"


    # Reference Field like Many2One but a field can refer to different model, foreight key is string and hold info about the corresponding model
    # the reference can change from model to another
    # it is a combination between ManyToOne and selection field
    # (model1, displayname1 ...)
    ref_if = fields.Reference(selection=[(
        'school.profile', 'School'), ('account.move', 'Invoice')], string="Reference Field")

    # perform soft delete using a flag
    active = fields.Boolean(string="Active", default=True)


    roll_number = fields.Char("Roll Number")

    @api.model
    def _change_roll_number(self, param):
        """ This method is called when install/upgrade a module to update the rollnumber"""
        print("Entered")
        for stud in self.search([('roll_number','=',False)]):
            stud.roll_number = "STD" + str(stud.id)

    # ORM method called when we click the save button while creating a record
    @api.model
    # @api.model_create_multi if we create multiple records vals_list will be a list of dict
    def create(self, vals_list):
        vals_list["active"] = True  # for exemple
        rlt = super().create(vals_list)
        print('/********************/')
        print(vals_list)
        # rlt.active=True we can also do this and change value after callinf the super method
        return rlt

    # ORM method called when we save while edit and at least a value IS CHANGED
    # vals will contain changed values set
    # no decorator is used from the version 13
    def write(self, vals):
        rlt = super().write(vals)
        print(vals)
        # i commented this because it raise issue when updating a module when already created data have no hobbies
        #if not self.hobby_list:
        #    raise UserError(_("Please select at least one hobby."))
        return rlt

    # ORM method called when duplicating a record
    # wa can use @api.returns('self', lambda v:v.id) decorator but no need
    def copy(self, default):
        default['active'] = False  # we can change values for duplicated fields
        rel = super().copy(default=default)
        return rel

    def unlink(self):

        for std in self:
            if std.student_fees > 0:
                raise UserError(_("can't delete student with fees"))

        rel = super().unlink()
        return rel

    # ORM method called to get fields with default attribute given or to set yours
    @api.model
    def default_get(self, fields_list):
        rel = super().default_get(fields_list)
        return rel

    # we start always with : obj = self.env['modelName']

    # search([('attribute','operator','value')])
    # elements = obj.search([])

    # we use browse orm method in the shel to get a record/list of records by id/list of ids
    # elements = obj.browse([1,2,3])

    # while search return the object and displaying the ids list of Integer, read method display the whole information : list of dict
    # elements = obj.read('attribute','operator','value')

    # ensure_one() raise error if we want to apply a custom method in None or multiple records
    def my_custom_method(self):
        self.ensure_one()  # will raise a valueError if self is None or having more than one record
        print(self.name)
    # elements = obj.search([])
    # elements.my_custom_method() we have many elements

    # elements.get_metadata() to get information like create_date, who create the record ... for all elements

    # while get_metadata is used on records to give information about those one
    # the fields_get is applayed to the modelObject and is giving info about the attribute like type (char,boolean..), required,readonly...
    # obj.fields_get()

    # read_group() to group records by attribute like in SQL
    # read_group([('field','op','value')],fields=['fieldToDisplay'],groupby=['fieldToGroupWith'])

    # field_view_get() will alow us to change the view attribute dynamically based on conditions

    # view_id in the view.xml
    # view_type is form/tree/calander/kanban...
    @api.model
    def fields_view_get(self, view_id, view_type, toolbar=False, submenu=False):
        """print("view_id",view_id)
        print("view_type",view_type)
        print("toolbar",toolbar)
        print("submenu",submenu)"""
        rlt = super().fields_view_get(view_id=view_id,
                                      view_type=view_type, toolbar=toolbar, submenu=submenu)

        if view_type == "form":
            doc = etree.XML(rlt['arch'])
            # we get the fild using xpath search
            name_field = doc.xpath("//field[@name='name']")
            if name_field:
                # this allow us to add element like fields, css...
                name_field[0].addnext(etree.Element(
                    'label', {'string': 'Hello'}))

            adress_field = doc.xpath("//field[@name='school_adress']")
            if adress_field:
                # we update an existing field
                adress_field[0].set('string', 'Hello 2')
                # as we added it to  in the view
                adress_field[0].set('nolabel', '0')

            rlt['arch'] = etree.tostring(doc, encoding="unicode")

        if view_type == "tree":
            doc = etree.XML(rlt['arch'])
            school_field = doc.xpath("//field[@name='school_id']")
            if school_field:
                school_field[0].addnext(etree.Element(
                    'field', {'string': 'Total fees', 'name': 'student_fees'}))

            rlt['arch'] = etree.tostring(doc, encoding="unicode")
        # in the result you find an arch attribute containing the fields
        # we can edit this to
        return rlt

    # we can create our one custom button
    def my_custom_button(self):
        print("Hello laslousa")
        # we create new cursor and user different env
        """new_cr = registry(self.env.cr.dbname).cursor()
        partner_id = self.env['res.partner'].with_env(self.env(cr=new_cr)).create({'name':"New env Prtner"})
        partner_id.env.cr.commit()"""

        # we can pass user authorization/permission restriction using the sudo()
        # self.env['table'].sudo().method()

    # we can use SQL statements here
    # self.env.cr.execute("select * from school_student")
    # self.env.cr.fetchall()

    # self.env.cr.execute("insert into school_student(name,school_id) values('fathi',5))
    # self.env.cr.commit()

    def open_fees_wiz(self):

        # this is the second way
        # as we have already created such info in the wizard, we can call it her
        # in the form wml we give the model.wizardActionInTargetModelId
        # for model we convert the . to _ as always as we are using _ as seperator between model and wizard
        return self.env['ir.actions.act_window']._for_xml_id("school_student.student_fees_update_action")

        # this the first way
        """return {"type": "ir.actions.act_window",
                "res_model": "student.fees.update.wizard",
                "view_mode": "form",
                "target": "new"} # target to open in the same screen or as pupup
                """

    # we use the tools library from odoo to get info from odoo config file
    # tools.config['attributeKey']


# for one to many it is different
# we have to add school as dependancy in the manifest first
# than we have to inherit the school and extend it by adding our fields
# this is normal as we may install school without installing student so no list od students to display
# but in case we istall student we have to install school and enable the view of students list in school

class SchoolProfile(models.Model):
    _inherit = "school.profile"  # the model _name in the school
    # we have to montion the model and the foreigh key (for bidirectional change)
    # limit to display only the n first element in the list
    student_list = fields.One2many(
        "school.student", "school_id", string="Students", limit=5)

    # we inherit an oddo core method to force creating at least one student when we create a school
    # the required field in the one2many will not work so we override this create method
    @api.model
    def create(self, vals_list):
        rlt = super().create(vals_list)
        if not rlt.student_list:
            raise UserError(_("please add at least a Student"))
        return rlt


class Hobbies(models.Model):
    _name = "hobby"
    name = fields.Char("Hobby")


class Partner(models.Model):
    _inherit = "res.partner"

    def create(self, vals_list):
        print(self.env)
        print(self.env.user)
        print(self.env.company)
        print(self.env.context)
        print(vals_list)

        # in shell we call obj = self.env['res.partner']  obj.create({name:'Partner'}) env.cr.commit()

        # we can use differnt context typing this in cmd
        # myContet = env.context.copy()
        # myContet['default_attribute']=value where attribute exist in the model
        # obj.with_context(myContet)create({name:'Partner with context'}) env.cr.commit()

        # here we use different ways, we do not apply with_context to the super

        # we can use different user to do operations
        # other_user = ser.env['res.user'].browse(6) we get the user with id=6
        # obj.with_user(other_user).create()...

        # with_company work the same

        return super(Partner, self.with_context(self.env.context)).create(vals_list)

# we also extend in the same model


class SchoolStudent(models.Model):
    _inherit = "school.student"
    parent_name = fields.Char(string="Parent Name")


# third name inheritence using many2one
class Car(models.Model):
    _name="car"
    name = fields.Char(string="Car")
    price = fields.Float(string="Price")

class CarEngine(models.Model):
    _name="car.engine"
    _inherits = {'car':'car_id'} # modelName:many2oneField
    name = fields.Char(string="Car Engine")
    car_id = fields.Many2one("car",string="Car")