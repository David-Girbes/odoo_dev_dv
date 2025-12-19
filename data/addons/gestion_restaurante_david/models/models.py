from odoo import models, fields, api


class plato_david(models.Model):
    _name = 'gestion_restaurante_david.plato_david'
    _description = 'suwiii'

    name = fields.Char(
        string="Nombre",
        help="nombre del plato",
        required=True

    )
    descripcion = fields.Text(
        string="Descripcion",
        help="desc del plato",
    )

    precio = fields.Float(
        string="Precio",
        help="precio del plato",
        required=True
    )
    tiempo_preparacion = fields.Integer(
        string="Tiempo",
        help="tiempo del plato",
        required=True
    )
    disponible = fields.Boolean(
        string="Disponible",
        help="disponibilidad del plato",
        default=True)
    
    categoria = fields.Selection(
        [
            ('entrante','Entrante'),
            ('principal','Principal'),
            ('postre','Postre'),
            ('bebida','Bebida')
        ],
        string="Selección",
        help="nombre del plato",
        required=True
    )


class menu_david(models.Model):
    _name = 'gestion_restaurante_david.menu_david'
    _description = 'gestion_restaurante_david.gestion_restaurante_david'



class ingredientes_david(models.Model):
    _name = 'gestion_restaurante_david.ingredientes_david'
    _description = 'gestion_restaurante_david.gestion_restaurante_david'

