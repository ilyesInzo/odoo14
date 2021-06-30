# -*- coding: utf-8 -*-
# from odoo import http


# class Hr-timesheet-astreinte(http.Controller):
#     @http.route('/hr-timesheet-astreinte/hr-timesheet-astreinte/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hr-timesheet-astreinte/hr-timesheet-astreinte/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hr-timesheet-astreinte.listing', {
#             'root': '/hr-timesheet-astreinte/hr-timesheet-astreinte',
#             'objects': http.request.env['hr-timesheet-astreinte.hr-timesheet-astreinte'].search([]),
#         })

#     @http.route('/hr-timesheet-astreinte/hr-timesheet-astreinte/objects/<model("hr-timesheet-astreinte.hr-timesheet-astreinte"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hr-timesheet-astreinte.object', {
#             'object': obj
#         })
