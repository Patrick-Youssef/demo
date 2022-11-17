# -*- coding: utf-8 -*-

{
    'name': 'CustomizeMe | 3D configurator',
    'category': 'Website/Website',
    'summary': 'Boost your sales and customer satisfaction with CustomizeMe for Odoo!',
    'website': 'https://customizeme.app/',
    'author': 'LetzCode',
    'version': '1.0.0',
    'description': """
Boost your sales and customer satisfaction with CustomizeMe for Odoo!
    """,
    'depends': ['website', 'sale', 'website_sale'],
    'images': ['static/description/img.png'],
    'data': [
        'security/ir.model.access.csv',
        'views/customizeme_product.xml',
        'views/customizeme_product_frontend.xml',
        'views/customizeme_settings.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
