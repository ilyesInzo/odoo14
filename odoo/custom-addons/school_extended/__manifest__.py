# -*- coding: utf-8 -*-
{
    'name': "school_extend",

    'summary': """
        school student inheritance""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['school_student'], # we use the _name after changing . to _

    # always loaded
    'data': [
        'views/student_extend_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
