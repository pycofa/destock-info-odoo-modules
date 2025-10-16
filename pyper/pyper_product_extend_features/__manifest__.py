# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Product extend features',
    'category': 'Extra Tools',
    'license': 'Other proprietary',
    'description': 'Add ability to extend product information with custom category features',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'installable': True,
    'depends': [
        'product',
        'pyper_product_catalog',
    ],
    'data': [
        # Menu
        'views/menu.xml',
        'views/product_template_views.xml',
    ],
}
