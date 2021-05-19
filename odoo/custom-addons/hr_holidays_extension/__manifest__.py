# -*- coding: utf-8 -*-
{
    'name': "hr_holidays_extend",

    'summary': """
        hr holidays inheritance""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Focus',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hr_holidays'], # we use the _name after changing . to _

    # always loaded
    'data': [
        'views/hr_leave_extend_views.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
