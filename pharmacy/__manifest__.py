{
    'name': 'Gestion de Pharmacie',
    'version': '1.0',
    'category': 'Healthcare',
    'summary': 'Gestion des pharmacies et des médicaments',
    'description': """
        Module principal de gestion de pharmacie:
        * Gestion des pharmacies
        * Gestion des médicaments
        * Gestion des stocks
        * Gestion des commandes
        * Gestion des médicaments équivalents
    """,
    'author': 'Jonah',
    'depends': [
        'base',
        'mail',
        # 'stock',
    ],
    'data': [
        'views/pharmacy_views.xml',
        'views/medecine_views.xml',
        'views/stock_views.xml',
        'views/order_views.xml',
        # 'data/pharmacy_data.xml',
        'views/menu_views.xml',
        'security/ir.model.access.csv',

    ],
    'demo': [
        'demo/pharmacy_demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
} 