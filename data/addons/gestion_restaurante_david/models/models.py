from odoo import models, fields,api


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
        required=True
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
    categoria = fields.Selection(
        [
            ('entrante', 'Entrante'),
            ('principal', 'Principal'),
            ('postre', 'Postre'),
            ('bebida', 'Bebida')
        ],
        string="Categoría",
        help="categoría del plato",
        required=True
    )

    codigo = fields.Char(compute="_get_codigo")

    precio_con_iva = fields.Float(compute="_compute_precio_iva")

    descuento = fields.Float(string="Descuento (%)",default=0)

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
    def _get_codigo(self):
        for plato in self:
            if not plato.categoria:
                plato.codigo = "PLT_" + str(plato.id)
            else:
                plato.codigo = str(plato.categoria[:3]).upper() + "_" + str(plato.id)

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
        string="Fecha Fin"
    )

    activo = fields.Boolean(
        string="Activo"
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
    @api.depends('platos', 'platos.precio_final')
    def _compute_precio_total(self):
        for menu in self:
            precios = menu.platos.mapped('precio_final')
            menu.precio_total = sum(precios)

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