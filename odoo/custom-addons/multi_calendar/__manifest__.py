# -*- coding: utf-8 -*-
{
    'name': "multi_calendar",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

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
    'depends': ['calendar'],

    # always loaded
    'data': [
        'views/assets.xml',
        'security/ir.model.access.csv',
        'data/calendar_data.xml',
        'data/calendar_event_update.xml',
        'views/views.xml',
        'views/menu.xml',
        'wizard/assigned_multi_employees_wizard_views.xml',
        'wizard/update_period_wizard_views.xml',
    ],
    'qweb': [
        'static/src/xml/template.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
