from odoo import models, fields


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
        Stirng="Descripción"
    )

    plato_ids = fields.Many2many(
        comodel_name = "gestion_restaurante_david.plato_david",
        relation = "plato_ingrediente_rel",
        column1='ingrediente_id',          
        column2='plato_id',
        string="Platos"
    )