{
    'name': 'Pharmacie Hospitalière',
    'version': '1.0',
    'category': 'Pharmacie',
    'summary': 'Gestion des commandes de médicaments pour l\'hôpital',
    'description': """
        Module de gestion des commandes de médicaments pour l'hôpital:
        * Suivi des stocks de médicaments de l'hôpital
        * Gestion des commandes auprès des pharmacies
        * Suivi des médicaments équivalents
        * Alertes de stock bas
    """,
    'author': 'Jonah',
    'depends': [
        'pharmacy',
        'hospital',
    ],
    'data': [
        'security/pharmacy_hospital_security.xml',
        'security/ir.model.access.csv',
        'views/hospital_pharmacy_views.xml',
        'views/hospital_order_views.xml',
        'views/hospital_menu_views.xml',
    ],
    'demo': [
        'demo/pharmacy_hospital_demo.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
} 