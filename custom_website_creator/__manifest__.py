{
    'name': 'Custom Website Creator',
    'version': '1.0',
    'summary': 'Customizable website features including quote request and CRM enhancements',
    'description': '''
        Ajoute des fonctionnalités personnalisées au site web Odoo, incluant des options de configuration,
        un formulaire de demande de devis, et des améliorations de la gestion des pistes CRM.
        Ce module permet une meilleure personnalisation du site et un meilleur suivi des leads.
    ''',
    'category': 'Website',
    'author': 'OBG',
    'website': 'https://www.obg.tn/',
    'license': 'LGPL-3',

    'images': [
        'static/description/banner.png'
    ],
    'depends': ['website', 'website_sale', 'web', 'crm', 'website_crm'],
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/crm_lead.xml',
        'views/cart_template.xml',
        'views/custom_form.xml',
        'views/res_config_website.xml',
        'views/demande_devis_view.xml',
        'views/confirmation_page.xml',
        'data/data.xml',
    ],

    'installable': True,
    'application': True,
}
