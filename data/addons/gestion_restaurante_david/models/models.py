from odoo import models, fields, api


class plato_david(models.Model):
    _name = 'gestion_restaurante_david.gestion_restaurante_david'
    _description = 'gestion_restaurante_david.gestion_restaurante_david'

    nombre = fields.Char()
    descripcion = fields.Text()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

