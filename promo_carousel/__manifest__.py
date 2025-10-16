# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).


{
    'name': 'Promos carousel',
    'category': 'Website/Website',
    'license': 'Other proprietary',
    'description': 'Create promos displayed on shop\'s carousel',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'installable': True,
    'depends': [
        # Base
        'website_sale',
        
        # Pyper
        'pyper_product_catalog',
    ],
    'data': [
        'views/promo_views.xml',
        'views/shop_views.xml',
        
        'security/ir.model.access.csv',
    ],
    'auto_install': ['website_sale', 'pyper_product_catalog'],
}
