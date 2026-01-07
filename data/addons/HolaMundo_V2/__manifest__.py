# HolaMundo_V1/__manifest__.py

{
    'name': 'Hola Mundo V2',
    'version': '1.0',
    'summary': 'Módulo básico de ejemplo',
    'description': 'Este es un módulo de ejemplo que no hace nada, solo sirve como plantilla.',
    'author': 'David',
    'category': 'Tools',
    'depends': [],
    'data': [
       'security/ir.model.access.csv',
        'views/hola_view.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}