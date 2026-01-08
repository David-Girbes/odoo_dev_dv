from datetime import timedelta
from odoo import models, fields, api


class gestion_tareas_david(models.Model):
    _name = 'gestion_tareas_david.gestion_tareas_david'
    _description = 'Gestión de Tareas'

    name = fields.Char(string='Nombre', required=True)

    codigo = fields.Char(compute="_get_codigo")

    descripcion = fields.Text(string='Descripción')

    fecha_creacion = fields.Date(string='Fecha de Creación', default=fields.Date.today, readonly=True)
    
    fecha_ini = fields.Date(string='Fecha de Inicio')

    fecha_fin = fields.Date(string='Fecha de Fin')

    finalizado = fields.Boolean(string='Finalizado', default=False)

    sprint = fields.Many2one(
        'gestion_tareas_david.sprints_david', 
        string='Sprint relacionado', 
        ondelete='set null', 
        help='Sprint al que pertenece esta tarea')
    
    rel_tecnologias = fields.Many2many(
        comodel_name='gestion_tareas_david.tecnologias_david',
        relation='relacion_tareas_tecnologias',
        column1='rel_tareas',
        column2='rel_tecnologias',
        string='Tecnologías')
    
    def _get_codigo(self):
        for tarea in self:
            # Si la tarea no tiene un sprint asignado
            if not tarea.sprint:
                tarea.codigo = "TSK_" + str(tarea.id)
            else:
                # Si tiene sprint, usamos su nombre
                tarea.codigo = str(tarea.sprint.name).upper() + "_" + str(tarea.id)


class sprints_david(models.Model):
    _name = 'gestion_tareas_david.sprints_david'
    _description = 'Modelo de Sprints para Gestión de Proyectos'

    name = fields.Char(string="Nombre", required=True)
    descripcion = fields.Text(string="Descripción")
    fecha_ini = fields.Datetime(string="Fecha Inicio", required=True)
    duracion = fields.Integer(
        string="Duración", 
        help="Cantidad de días que tiene asignado el sprint")

    fecha_fin = fields.Datetime(
        compute='_compute_fecha_fin', 
        store=True,
        string="Fecha Fin")
    
    tareas = fields.One2many(
        comodel_name='gestion_tareas_david.gestion_tareas_david',
        inverse_name='sprint',
        string='Tareas')

    @api.depends('fecha_ini', 'duracion')
    def _compute_fecha_fin(self):
        for sprint in self:
            if sprint.fecha_ini and sprint.duracion and sprint.duracion > 0:
                sprint.fecha_fin = sprint.fecha_ini + timedelta(days=sprint.duracion)
            else:
                sprint.fecha_fin = sprint.fecha_ini
    
    


class tecnologias_david(models.Model):
    _name = 'gestion_tareas_david.tecnologias_david'
    _description = 'Tecnologías'

    name = fields.Char(
        string="Nombre", 
        required=True, 
        help="Nombre de la tecnología")

    descripcion = fields.Text(
        string="Descripción", 
        help="Descripción de la tecnología")

    logo = fields.Image(
        string="Logo", 
        max_width=256, 
        max_height=256,
        help="Logo de la tecnología (máximo 256x256 píxeles)")
    
    rel_tareas = fields.Many2many(
        comodel_name='gestion_tareas_david.gestion_tareas_david',
        relation='relacion_tareas_tecnologias',
        column1='rel_tecnologias',
        column2='rel_tareas',
        string='Tareas')