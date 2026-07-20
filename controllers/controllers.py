# -*- coding: utf-8 -*-
# from odoo import http


# class Openlibrary(http.Controller):
#     @http.route('/openlibrary/openlibrary/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/openlibrary/openlibrary/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('openlibrary.listing', {
#             'root': '/openlibrary/openlibrary',
#             'objects': http.request.env['openlibrary.openlibrary'].search([]),
#         })

#     @http.route('/openlibrary/openlibrary/objects/<model("openlibrary.openlibrary"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('openlibrary.object', {
#             'object': obj
#         })
