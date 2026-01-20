from datetime import datetime, timedelta
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

#TAREAS------------------------------------------------------
class gestion_tareas_david(models.Model):
    _name = 'gestion_tareas_david.gestion_tareas_david'
    _description = 'Gestión de Tareas'

    name = fields.Char(string='Nombre', required=True)

    codigo = fields.Char(compute="_get_codigo")

    descripcion = fields.Text(string='Descripción')


    fecha_creacion = fields.Date(string='Fecha de Creación', default=lambda self: datetime.now(), readonly=True)
    
    fecha_ini = fields.Date(string='Fecha de Inicio')

    fecha_fin = fields.Date(string='Fecha de Fin')

    finalizado = fields.Boolean(string='Finalizado', default=False)

    sprint = fields.Many2one(
        'gestion_tareas_david.sprints_david', 
        string='Sprint relacionado', 
        compute="_compute_sprint",
        store=True, 
        help='Sprint al que pertenece esta tarea')
    
    rel_tecnologias = fields.Many2many(
        comodel_name='gestion_tareas_david.tecnologias_david',
        relation='relacion_tareas_tecnologias',
        column1='rel_tareas',
        column2='rel_tecnologias',
        string='Tecnologías')
    
    historia = fields.Many2one(
        'gestion_tareas_david.historias_david',
        string="Historia de la tarea",
        ondelete='set null',
    )

    def _get_proyecto_activo(self):
        return self.env['gestion_tareas_david.proyectos_david'].search(
        [('activo', '=', True)], 
        limit=1, order='create_date desc')
    

    proyecto = fields.Many2one(
        'gestion_tareas_david.proyectos_david',
        string='Proyecto',
        related='historia.proyecto',
        readonly=True,
        default=_get_proyecto_activo)
    
    proyecto_default = fields.Many2one(
        'gestion_tareas_david.proyectos_david',
        string='Proyecto default',
        default=_get_proyecto_activo)
    
    responsable = fields.Many2one(
        'res.users',
        string='Responsable',
        default=lambda self: self.env.user.id)
    

    
    @api.depends('sprint','sprint.name')
    def _get_codigo(self):
        _logger.info("Iniciando generación de códigos de tareas")

        for tarea in self:
            try:
                if not tarea.sprint:
                    _logger.warning(f"Tarea {tarea.id} sin sprint asignado")
                    tarea.codigo = "TSK_" + str(tarea.id)

                else:
                    # Si tiene sprint, usamos su nombre
                    tarea.codigo = str(tarea.sprint.name).upper() + "_" + str(tarea.id)

                _logger.debug(f"Código generado: {tarea.codigo}")

            except Exception as e:
                _logger.error(f"Error generando código para tarea {tarea.id}: {str(e)}")
                raise ValidationError(f"Error al generar el código: {str(e)}")

    @api.depends('historia', 'historia.proyecto')
    def _compute_sprint(self):
        for tarea in self:
            tarea.sprint = False

            # Verificar que la tarea tiene historia y proyecto
            if tarea.historia and tarea.historia.proyecto:
                # Buscar sprints del proyecto
                sprints = self.env['gestion_tareas_david.sprints_david'].search([
                    ('proyecto.id', '=', tarea.historia.proyecto.id)
                ])

                # Buscar el sprint activo (fecha_fin > ahora) 
                # de entre todos los sprints asociados al proyecto
                # en teoría solo hay un sprint activo, por eso es el que no ha vencido
                for sprint in sprints:
                    if (isinstance(sprint.fecha_fin, datetime) and 
                            sprint.fecha_ini <= datetime.now() and   
                            sprint.fecha_fin > datetime.now()):
                        tarea.sprint = sprint.id
                        break

#PROYECTOS-----------------------------------------------------
class proyectos_david(models.Model):
    _name = 'gestion_tareas_david.proyectos_david'
    _description = 'Gestión Proyectos'

    name = fields.Char(
        string="Nombre",
        required=True
    )

    descripcion = fields.Text(
        string="Descripción"
    )

    historias = fields.One2many(
        comodel_name='gestion_tareas_david.historias_david',
        inverse_name='proyecto',
        string='Historias del proyecto')
    
    sprints = fields.One2many(
        'gestion_tareas_david.sprints_david',
        'proyecto',
        string="Sprints"
    )

    activo = fields.Boolean(
    string= "Estado del proyecto",
    default = True
) 
    
    

#HISTORIAS------------------------------------------------------
class historias_david(models.Model):
    _name = 'gestion_tareas_david.historias_david'
    _description = "Historias"

    name = fields.Char(
        string="Nombre",
        required=True
    )

    descripcion = fields.Text(
        string="Descripción"
    )

    proyecto = fields.Many2one(
        'gestion_tareas_david.proyectos_david', 
        string='Proyecto', 
        ondelete='set null', 
        help='Proyecto a que pertenece')
    
    tareas = fields.One2many(
        comodel_name='gestion_tareas_david.gestion_tareas_david',
        inverse_name='historia',
        string='Tareas de la historia')
    
    tecnologias = fields.Many2many(
        "gestion_tareas_david.tecnologias_david", 
        compute="_compute_tecnologias", 
        string="Tecnologías Utilizadas")

    @api.depends('tareas', 'tareas.rel_tecnologias')
    def _compute_tecnologias(self):
        for historia in self:
            tecnologias_acumuladas = self.env['gestion_tareas_david.tecnologias_david']

            # Recorrer todas las tareas de la historia
            for tarea in historia.tareas:
                # Sumar (concatenar) tecnologías de cada tarea
                tecnologias_acumuladas = tecnologias_acumuladas + tarea.rel_tecnologias

            # Asignar el resultado
            historia.tecnologias = tecnologias_acumuladas

#SPRINTS----------------------------------------------------------
class sprints_david(models.Model):
    _name = 'gestion_tareas_david.sprints_david'
    _description = 'Modelo de Sprints para Gestión de Proyectos'

    name = fields.Char(string="Nombre", required=True)
    descripcion = fields.Text(string="Descripción")
    fecha_ini = fields.Datetime(string="Fecha Inicio", required=True)
    duracion = fields.Integer(
        string="Duración", 
        default=14,
        help="Cantidad de días que tiene asignado el sprint")

    fecha_fin = fields.Datetime(
        compute='_compute_fecha_fin', 
        store=True,
        string="Fecha Fin")
    
    tareas = fields.One2many(
        comodel_name='gestion_tareas_david.gestion_tareas_david',
        inverse_name='sprint',
        string='Tareas')
    
    proyecto = fields.Many2one(
        'gestion_tareas_david.proyectos_david',
        string="Proyecto",
        ondelete="set null"
    )

    @api.depends('fecha_ini', 'duracion')
    def _compute_fecha_fin(self):
        for sprint in self:
            if sprint.fecha_ini and sprint.duracion and sprint.duracion > 0:
                sprint.fecha_fin = sprint.fecha_ini + timedelta(days=sprint.duracion)
            else:
                sprint.fecha_fin = sprint.fecha_ini
    
    

#TECNOLOGIAS---------------------------------------------------------------
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