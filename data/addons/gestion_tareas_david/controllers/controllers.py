# from odoo import http


# class GestionTareasDavid(http.Controller):
#     @http.route('/gestion_tareas_david/gestion_tareas_david', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gestion_tareas_david/gestion_tareas_david/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('gestion_tareas_david.listing', {
#             'root': '/gestion_tareas_david/gestion_tareas_david',
#             'objects': http.request.env['gestion_tareas_david.gestion_tareas_david'].search([]),
#         })

#     @http.route('/gestion_tareas_david/gestion_tareas_david/objects/<model("gestion_tareas_david.gestion_tareas_david"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gestion_tareas_david.object', {
#             'object': obj
#         })

