# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).


{
    'name': 'Link to public categories',
    'category': 'Website/Website',
    'license': 'Other proprietary',
    'description': 'Link between categories and public categories in website sale',
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
        'views/product_public_category_views.xml',
        'views/product_category_views.xml',
        'views/shop_views.xml',
    ],
    'auto_install': ['website_sale'],
}
