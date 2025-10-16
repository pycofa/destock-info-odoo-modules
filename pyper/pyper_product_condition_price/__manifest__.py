# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Product condition price',
    'category': 'Manufacturing/Repair',
    'license': 'Other proprietary',
    'description': 'This addon adds ability to manage product condition custom prices.',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'installable': True,
    'depends': [
        'product',
        'pyper_product_condition',
    ],
    'data': [
        # Security
        'security/product_security.xml',

        # Views
        'views/conf_setting_views.xml',
        'views/product_product_views.xml',
        'views/product_template_views.xml',
    ],
}
