# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).


{
    'name': 'Remove background of the product\'s image',
    'category': 'Website/Website',
    'license': 'Other proprietary',
    'description': 'Remove background image',
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
    ],
    'data': [
        'views/product_template_views.xml',
        'views/res_config_settings_views.xml',
    ],
    'auto_install': ['website_sale'],
}
