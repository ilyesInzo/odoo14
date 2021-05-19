# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'School',
    'version': '1.1',
    'category': 'Schools',
    'summary': 'Test School',
    'description': """
This contain schools
    """,
    'depends': ['base'],
    'data': [
        'views/school_view.xml',
        'security/ir.model.access.csv'
    ],
    'demo': [
    ],
    'installable': True,
    'auto_install': False
}
