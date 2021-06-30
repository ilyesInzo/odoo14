# -*- coding: utf-8 -*-
{
    'name': "project_extend",

    'summary': """
        project inheritance""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Focus",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '1.0.1',

    # any module necessary for this one to work correctly
    'depends': ['project'], # we use the _name after changing . to _

    # always loaded
    'data': [
        'security/project_extend_security.xml',
        'security/ir.model.access.csv',
        'views/project_extension_views.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
