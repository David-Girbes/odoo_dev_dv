import datetime
from odoo import models,fields,api
from .logica_dronify import calcular_consumo_vuelo,validar_estado_bateria
from odoo.exceptions import ValidationError


#DRON---------------------------------------------------------
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
        string="Batería",
        help="Nivel de carga del dron",
        default=100
    )

    estado = fields.Selection(
        [("disponible","Disponible"),
        ("vuelo","Vuelo"),
        ("taller","Taller")],
        string="Estado",
        default="disponible"
    )

    piloto_autorizado_ids = fields.Many2many(
        'res.partner',
        'pilotos_drones_rel',
        column1="dron_id",
        column2="piloto_id",
        string="Pilotos",
        domain=[('es_piloto','=',True)]
    )


#CONTACTO---------------------------------------------------------

class contacto(models.Model):
    _name="res.partner"
    _inherit="res.partner"

    es_cliente = fields.Boolean(
        string="Es Cliente"
    )

    es_vip = fields.Boolean(
        string="Es Vip"
    )

    es_piloto = fields.Boolean(
        string="Es Piloto"
    )

    licencia = fields.Char(
        string="Licencia"
    )

    dron_autorizado_ids = fields.Many2many(
        'dronify.dron',
        'pilotos_drones_rel',
        column1="piloto_id",
        column2="dron_id",
        string="Drones"
    )



#PAQUETE---------------------------------------------------------
class paquete(models.Model):
    _name="dronify.paquete"
    _description="Paquetes de dronify"

    codigo = fields.Char(
        string="Código",
        compute="_compute_codigo",
        readonly=True
    )

    name = fields.Char(
        string="Nombre",
        required=True
    )

    peso = fields.Float(
        required=True,
        string="Peso"
    )

    cliente_id = fields.Many2one(
        'res.partner',
        string="Cliente",
        ondelete="set null"
    )

    vuelo_id = fields.Many2one(
        'dronify.vuelo',
        string="Vuelo",
        ondelete="set null"
    )

    dron_relacionado = fields.Char(
        string="Dron",
        related="vuelo_id.dron_id.name"
    )

    @api.depends('create_date')
    def _compute_codigo(self):
        for paquete in self:
            fecha_str = paquete.create_date or fields.Datetime.now()
            paquete.codigo = fecha_str.strftime("%Y%m%d%H%M%S")
            

#VUELO---------------------------------------------------------
class vuelo(models.Model):
    _name="dronify.vuelo"
    _description="Vuelos"

    codigo = fields.Char(
        compute="_compute_codigo",
        string="Código",
        readonly=True,
    )

    def _compute_name_default(self):
            ahora = fields.Datetime.now() 
            fecha_str = ahora.strftime("%Y%m%d%H%M%S")
            return f"{fecha_str}-Vuelo"

    name = fields.Char(
        string="Nombre",
        default=_compute_name_default,
        required=True
    )

    preparado = fields.Boolean(
        string="Preparado",
        readonly=True
    )

    realizado = fields.Boolean(
        string="Realizado",
        readonly=True
    )

    paquetes_ids = fields.One2many(
        'dronify.paquete',
        inverse_name="vuelo_id",
        string="Paquetes"
    )

    dron_id = fields.Many2one(
        'dronify.dron',
        string="Dron",
        ondelete="set null"
    )

    piloto_id = fields.Many2one(
        'res.partner',
        string="Piloto",
        ondelete="set null",
        domain=[('es_piloto','=',True)]
    )

    peso_total = fields.Float(
        string="Peso Total",
        compute="_compute_peso_total",
        store=True
    )

    consumo_estimado = fields.Float(
        string="Consumo",
        compute="_compute_consumo",
        store=True
    )

    @api.depends('paquetes_ids.peso')
    def _compute_consumo(self):
        for vuelo in self:
            vuelo.consumo_estimado = calcular_consumo_vuelo(vuelo.peso_total)
        
    @api.depends('create_date')
    def _compute_codigo(self):
        for vuelo in self:
            if vuelo.create_date:
                fecha_str = vuelo.create_date.strftime('%Y%m%d%H%M%S')
                vuelo.codigo = f"{fecha_str}"
            

    def preparar_vuelo(self):
        for vuelo in self:
                
            if not vuelo.piloto_id and not vuelo.dron_id:
                raise ValidationError("Tienes que poner dron y piloto")
            
            if not vuelo.paquetes_ids:
                raise ValidationError("Tiene que tener algún paquete")
            
            if vuelo.peso_total > vuelo.dron_id.capacidad_max:
                raise ValidationError("El peso es superior a la capacidad del dron")
            
            if vuelo.dron_id.estado != 'disponible':
                raise ValidationError("El dron debe estar disponible")

            if not validar_estado_bateria(vuelo.dron_id.bateria, vuelo.consumo_estimado):
                raise ValidationError("La batería debe ser mayor al consumo")
            
            if vuelo.dron_id not in vuelo.piloto_id.dron_autorizado_ids:
                raise ValidationError("Ese piloto no tiene ese dron asignado")
            
            vuelo.preparado = True

            vuelo.dron_id.estado = 'vuelo'

    def desbloquear(self):
        for vuelo in self:
            vuelo.preparado = False
            vuelo.dron_id.estado = 'disponible'

    def realizar_vuelo(self):
        for vuelo in self:
            vuelo.dron_id.bateria = vuelo.dron_id.bateria - vuelo.consumo_estimado
            vuelo.dron_id.estado = 'disponible'

            vuelo.realizado = True


    @api.depends('paquetes_ids.peso')
    def _compute_peso_total(self):
        for vuelo in self:
            peso_total_c = 0
            for paquete in vuelo.paquetes_ids:
                peso_total_c += paquete.peso
            vuelo.peso_total = peso_total_c
     


    




