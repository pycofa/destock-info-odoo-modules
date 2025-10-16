# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).


{
    'name': 'Disable website sale cart',
    'category': 'Website/Website',
    'license': 'Other proprietary',
    'description': 'Allow to disabled add to cart in the sop',
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
        'views/conf_settings_views.xml',
        'views/disable_cart_views.xml',
    ],
    'auto_install': True,
}
