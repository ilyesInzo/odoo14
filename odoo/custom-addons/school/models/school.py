from odoo import api, fields, models


class SchoolProfile(models.Model):
    # this will create a table with the given name in DB
    # the . will be converted to _ in the Table name : school_profile
    _name = "school.profile"
    _rec_name="email" # the email will be diplayed in selections,list... (if name_get not overriten)
    # to add a default order for the elements, we give an attribute
    # _order='email asc, phone desc' #by default asc
    # char is a data types, name is the proporty (column name by default if no argument given to the data type)
    # in our case the column name will be School name
    # help="this field is..." to add tooltip to the label field
    # readonly=true to read only
    # required=true
    # default="value"
    # size=value the max field lenght
    # index=True to index the field in db
    # trim=False to enable adding empty space at start and the end after saving

    # We can do the above change in front side in the view
    # With copy= False we will remain the name field blank when duplicating a school
    name = fields.Char(string="School name", help="this is the school name", copy=False)
    email = fields.Char(string="Email")
    phone = fields.Char("phone")
    # like the other fields we can montion some properties like default, readonly required...
    is_virtual_school = fields.Boolean(string="Is Virtual")
    # number after and before the .
    result = fields.Float(string="Result", digits=(2, 3))
    school_rank = fields.Integer(string="Rank")
    address = fields.Text(string="address", help="this is an AreaText field")

    open_date = fields.Datetime("open date", default=fields.Datetime.now())

    def giveDefaultEstablishDate(self):
        return fields.Date.today()

    # backend format is YYYY-MM-DD != from frontend
    establish_date = fields.Date(
        "establish date", default=lambda m: m.giveDefaultEstablishDate())

    # we use a list of tuple ('field tobe stored in database','label')
    # we use first key for default value
    school_type = fields.Selection([('public', 'Public School'), (
        'private', 'Private School')], string="School Type", default="private")

    documents = fields.Binary(string="Documents")
    doc_name = fields.Char(string="File Name")
    # verifi reso is by default true, if added false the image will be treated as binary like any file
    school_image = fields.Image(
        "Add image", max_width=100, max_height=100, verify_resolution=True)
    # like Text but with additional text format : bold,iltalic...
    school_description = fields.Html(string="HTML")

    # compute field to change behaviour based on other attribute change
    auto_rank = fields.Integer(compute="_change_auto_rank", string="Auto Rank") #add store=true if we want to save the field

    # the name should be unique, if there are alreadu records who do not respect he constraint, module upgrade will fail
    #_sql_constraints = [('_name_unique','unique (name)','Please enter unique name')]

    # with the depends decorator, the rank will be changed when selecting. withour this the rank is calculate after create/edit clicked
    @api.depends("school_type")
    def _change_auto_rank(self):
        for res in self:
            if res.school_type == "public":
                res.auto_rank += res.school_rank + 20
            elif res.school_type == "private":
                res.auto_rank += res.school_rank + 30
            else:
                res.auto_rank = res.school_rank

    # orm method called when we create a record from a selection list for exemple
    @api.model
    def name_create(self, name):
        rlt = super().name_create(name)
        print(rlt.name_get())
        return rlt
    # no need to call the super in reality, we can do something like:
    """@api.model
    def name_create(self, name):
        rlt = super().create({"name":name, "email":'aaa@zzz.ddd'})
        return rlt.name_get()[0]"""

    # used to give more information in the selection field when selecting a school for exemple
    # if we add an attribute _rec_name="atrributeTo display than we will have the attribute value displayed instead of value of name attribute"
    def name_get(self):

        #rlt = super().name_get()

        o = []

        for school in self:
            # we can also do some check based on the context field to give different display
            custom_name = school.name
            if school.school_type:
                custom_name += " ({})".format(school.school_type)
            o.append((school.id,custom_name))
        return o       


    # we use this method to add more filter capability/autocomplition for additional fields when selecting an element
    # by default the name is used
    # there is another method _name_search which have an additional attribute for the id_user who perform the search
    # and this methode is calling the bellow one that we overriten
    @api.model
    def name_search(self, name, args, operator, limit):

        args =  args or []
        if name:
            rslt = self.search(['|',('name',operator,name), ('email',operator,name)])
            return rslt.name_get()

        return super().name_search(name=name, args=args, operator=operator, limit=limit)

    # list = obj.search([])
    # list_ids = list.ids we retrieve the ids like that
    # but with object._search([]) this give us the list of ids directly
    # we can use filtered method on the retrieved list instead of calling search 
    # list.filtered(lambda a : booleanExpression)


    # mapped fuction is similar to Map in python 
    # the result is without redandent elements
    # list = obj.search([])
    # list.mapped(lambda a : returnValue)

    # sorted method
    # list = obj.search([])
    # list.sorted(key="id") like the _order="attribute" we give also the attribute her
    # we can also use lambda function
    # list.sorted(lambda a : a.attribute)

    



