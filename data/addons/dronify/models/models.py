from odoo import models,fields,api



class dron(models.Model):

    _name="dronify.dron"
    _description="Drones"

    name = fields.Char(
        string="Nombre"
    )

    capacidad_max = fields.Float(
        string="Capacidad Máxima",
        help="Carga máxima en kilogramos",
        required=True
    )

    bateria = fields.Integer(
        string="Carga",
        help="Nivel de carga del dron",
        default=100
    )

    estado = fields.Selection(
        (["disponible","Disponible"],
        ["vuelo","Vuelo"],
        ["taller","Taller"]),
        string="Estado",
        default="disponible"
    )

class contacto(models.Model):
    _name="res.partner"
    _inherit="res.partner"

    es_cliente = fields.Boolean(
        string="Es Camarero"
    )

    es_vip = fields.Boolean(
        string="Es Vip"
    )

    es_piloto = fields.Boolean(
        string="Es Piloto"
    )

    licencia = fields.Char(
        string="Licencia",
    )

    




