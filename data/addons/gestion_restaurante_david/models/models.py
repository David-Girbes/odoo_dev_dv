from datetime import datetime, timedelta
from odoo import models, fields,api
from odoo.exceptions import ValidationError,UserError
import logging

_logger = logging.getLogger(__name__)

#PLATO-----------------------------------------------------------------
#----------------------------------------------------------------------
class plato_david(models.Model):
    _name = 'gestion_restaurante_david.plato_david'
    _description = 'Platos del restaurante'

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
        required=True,
        default=5.0
    )
    tiempo_preparacion = fields.Integer(
        string="Tiempo preparación",
        help="tiempo del plato",
        required=True
    )
    disponible = fields.Boolean(
        string="Disponible",
        help="disponibilidad del plato",
        default=True
    )

    fecha_alta = fields.Date(
        string="Fecha Alta",
        default= lambda self: fields.Date.today()
    )
    

    codigo = fields.Char(compute="_get_codigo")

    precio_con_iva = fields.Float(compute="_compute_precio_iva")

    descuento = fields.Float(string="Descuento (%)",default=0.0)

    precio_final = fields.Float(
        compute="_compute_precio_final",
        store=True,
        string = "Precio Final")

    menu_id = fields.Many2one(
        comodel_name="gestion_restaurante_david.menu_david",
        string="Menú",
        help="Menú al que pertenece este plato",
        ondelete='set null'
    )

    ingrediente_ids = fields.Many2many(
        comodel_name="gestion_restaurante_david.ingredientes_david",
        relation="plato_ingrediente_relation",
        column1="plato_id",
        column2="ingrediente_id",
        string="Ingredientes"
    )

    
    def _get_categoria_defecto(self):
            return self.env['gestion_restaurante_david.categorias_david'].search([('name','=','Sin Clasificar')],limit=1)


    categoria_id = fields.Many2one(
        'gestion_restaurante_david.categorias_david',
        string="Categoria",
        ondelete="set null",
        default=_get_categoria_defecto
    )
    chef_especializado = fields.Many2one(
        'gestion_restaurante_david.chef_david',
        compute="_compute_chef_especializado",
        store=True,
    )

#MÉTODOS-----------------------------------------------------------------

    @api.depends('categoria_id')
    def _compute_chef_especializado(self):
        for plato in self:
            if plato.categoria_id:
                chef = self.env['gestion_restaurante_david.chef_david'].search([('especialidad_id', '=', plato.categoria_id.id)],limit=1)
                if chef:
                    plato.chef_especializado = chef
                else:
                    plato.chef_especializado = False
            else:
                plato.chef_especializado = False


    @api.depends('categoria_id')
    def _get_codigo(self):
        try:
            for plato in self:
                if not plato.categoria_id:
                    _logger.warning(f"Plato {plato.name} sin categoría")
                    plato.codigo = "PLT_" + str(plato.id)
                    
                else:
                    plato.codigo = str(plato.categoria_id.name).upper() + "_" + str(plato.id)

                _logger.debug(f"Se le asigna el codigo {plato.codigo}")

        except Exception as e:
            _logger.error(f"Error generando el código para plato {plato.id}: {str(e)}")
            raise ValidationError(f"Error al generar el codigo: {str(e)}")

#DEPENDS-----------------------------------------------------------------
    @api.depends('precio')
    def _compute_precio_iva(self):
        for plato in self:
            if plato.precio:
                plato.precio_con_iva = plato.precio * 1.10
            else:
                plato.precio_con_iva = 0.0

    @api.depends('precio', 'descuento')
    def _compute_precio_final(self):
        for plato in self:
            if plato.precio:
                if plato.descuento:
                    plato.precio_final = plato.precio * (1 - plato.descuento / 100)
                else:
                    plato.precio_final = plato.precio
            else:
                plato.precio_final = 0.0

#CONSTRAINS-----------------------------------------------------------------
    @api.constrains('precio')
    def _check_precio_positivo(self):
        for plato in self:
            if plato.precio <= 0:
                raise ValidationError("El precio del plato no puede ser menor o igual a 0")

    @api.constrains('tiempo_preparacion')
    def _check_preparacion(self):
        for plato in self:
            if plato.tiempo_preparacion:
                if plato.tiempo_preparacion < 1 or plato.tiempo_preparacion > 240:
                    raise ValidationError("El tiempo de preparación debe estar entre 1 y 240")


#MENU-----------------------------------------------------------------
#---------------------------------------------------------------------
class menu_david(models.Model):
    _name = 'gestion_restaurante_david.menu_david'
    _description = 'Menús del restaurante'

    name = fields.Char(
        string="Nombre del Menú", required=True,
        )
    
    descripcion = fields.Text(
        string="Descripción",

    )

    fecha_inicio = fields.Date(
        string="Fecha de inicio",
        required=True
        
    )

    fecha_fin = fields.Date(
        string="Fecha Fin",
        compute="_compute_fecha_fin"
    )

    dias_disponible = fields.Integer(
        string="Dias disponible",
        default=7
    )

    activo = fields.Boolean(
        string="Activo",
        default=False
    )

    creado_por = fields.Many2one(
        'res.users',
        string="Creado por",
        default= lambda self: self.env.user.id,
        readonly=True

    )

    platos = fields.One2many(
        comodel_name="gestion_restaurante_david.plato_david",
        inverse_name="menu_id",
        string="Platos",
        help="Platos que pertenecen a este menú" 
    )

    precio_total = fields.Float(
        string="Precio Total",
        compute="_compute_precio_total",
        store=True
    )

    
            

#DEPENDS-----------------------------------------------------------------
    @api.depends('fecha_inicio', 'dias_disponible')
    def _compute_fecha_fin(self):
        for menu in self:
            if menu.fecha_inicio:
                menu.fecha_fin = menu.fecha_inicio + timedelta(days=menu.dias_disponible)
            else:
                menu.fecha_fin = False

    @api.depends('platos', 'platos.precio_final')
    def _compute_precio_total(self):
        for menu in self:
            precios = menu.platos.mapped('precio_final')
            menu.precio_total = sum(precios)

#CONSTRAINS-----------------------------------------------------------------
    @api.constrains('fecha_fin','fecha_inicio')
    def _check_fecha(self):
        for menu in self:
            if menu.fecha_fin:
                if menu.fecha_fin < menu.fecha_inicio:
                    raise ValidationError("La Fecha fin debe ser posterior a la fecha de inicio")
                
    @api.constrains('platos','activo')
    def _check_plato(self):
        for menu in self:
            if menu.activo and len(menu.platos) <= 0:
                raise ValidationError("No puede haber un menú sin platos")
            

#CHEF------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class chef_david(models.Model):
    _name= 'gestion_restaurante_david.chef_david'
    _description = 'sigma'

    name = fields.Char(
        string="Nombre",
        required=True
    )

    especialidad_id = fields.Many2one(
        'gestion_restaurante_david.categorias_david',
        string="Especialidad",
        ondelete="set null"
    )

    platos_asignados = fields.One2many(
        'gestion_restaurante_david.plato_david',
        'chef_especializado',
        string="Platos Asignados"
    )

            
#CATEGORIAS-----------------------------------------------------------------
#-----------------------------------------------------------------------------
class categorias_david(models.Model):
    _name= 'gestion_restaurante_david.categorias_david'
    _description = 'sigma'

    name = fields.Char(
        string="Nombre",
        required=True
    )

    descripcion = fields.Text(
        string="Descripción"
    )

    platos_ids = fields.One2many(
        'gestion_restaurante_david.plato_david',
        'categoria_id',
        string="Platos"
    )

    chef_ids = fields.One2many(
        'gestion_restaurante_david.chef_david',
        'especialidad_id',
        string="Chefs"

    )

    ingredientes_comunes = fields.Many2many(
        'gestion_restaurante_david.ingredientes_david',
        relation="rel_categorias_ingredientes",
        compute="_compute_ingredientes_comunes",
        string="Ingredientes comunes"

    )


#INGREDIENTES-----------------------------------------------------------------
#-----------------------------------------------------------------------------

class ingredientes_david(models.Model):
    _name = 'gestion_restaurante_david.ingredientes_david'
    _description = 'Ingredientes del restaurante'

    name = fields.Char(
        string="Nombre",
        required=True
    )

    es_alergeno = fields.Boolean(
        string="Alergeno"
    )

    descripcion = fields.Text(
        string="Descripción"
    )

    plato_ids = fields.Many2many(
        comodel_name = "gestion_restaurante_david.plato_david",
        relation = "plato_ingrediente_rel",
        column1='ingrediente_id',          
        column2='plato_id',
        string="Platos"
    )