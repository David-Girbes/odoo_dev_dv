# from odoo import http


# class GestionRestauranteDavid(http.Controller):
#     @http.route('/gestion_restaurante_david/gestion_restaurante_david', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gestion_restaurante_david/gestion_restaurante_david/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('gestion_restaurante_david.listing', {
#             'root': '/gestion_restaurante_david/gestion_restaurante_david',
#             'objects': http.request.env['gestion_restaurante_david.gestion_restaurante_david'].search([]),
#         })

#     @http.route('/gestion_restaurante_david/gestion_restaurante_david/objects/<model("gestion_restaurante_david.gestion_restaurante_david"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gestion_restaurante_david.object', {
#             'object': obj
#         })

