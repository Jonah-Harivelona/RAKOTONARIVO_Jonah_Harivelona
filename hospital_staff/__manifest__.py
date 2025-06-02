{
    'name' : 'Hospital Staff',
    'version': '1.0',
    'depends' : ['base'],
    'author': 'Jonah',
    'category': 'Hospital Staff',
    'summary': 'Personnelle médicale',
    'description': "Personnelle médicale",
    'data': [
        'views/hospital_staff_menu_views.xml',
        'views/hospital_staff_doctor_views.xml',
        'views/hospital_staff_infirmier_views.xml',
        'security/ir.model.access.csv',
        
    ],
    'installable': True,
    'application': True,
}