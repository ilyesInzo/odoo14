# -*- coding: utf-8 -*-
{
    'name': "project_template",

    'summary': """
        Create projects from templates
        """,

    'description': """
        Offer the possibility to create/init project from a project template
    """,

    'author': "Focus",
    'website': "http://www.focus-corporation.com",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['project_extension'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/project_template_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
