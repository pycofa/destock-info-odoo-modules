# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).


{
    'name': 'Show only available attributes in ecommerce',
    'category': 'Website/Website',
    'license': 'Other proprietary',
    'description': 'Show only available attributes in ecommerce',
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
        
        'website_sale_disable_cart',
    ],
    'data': [
        'views/product_attributes_views.xml',
		'views/shop_views.xml',
        'views/product_views.xml',
        'views/conf_settings_views.xml',

        'security/website_sale_show_qty_security.xml',
    ],
    'auto_install': True,
}
