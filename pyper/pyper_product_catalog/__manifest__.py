# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).
{
    'name': 'Product catalog',
    'category': 'Inventory/Inventory',
    'license': 'Other proprietary',
    'description': 'Addon dedicated to product catalog management',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'depends': [
        'product',
		'pyper_menu',
    ],
    'data': [
        # Security
        'security/ir.model.access.csv',

        # Views
        'views/product_views.xml',
        'views/product_manufacturer_views.xml',
        'views/menu.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'pyper_product_catalog/static/src/scss/style.scss',
        ],
    }
}
