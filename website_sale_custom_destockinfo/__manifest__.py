# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).


{
    'name': 'Destock custom website sale',
    'category': 'Website/Website',
    'license': 'Other proprietary',
    'description': 'Destock custom shop',
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
        'website_sale_only_available_attributes',
        'destockinfo_website'
    ],
    'data': [
        'views/filters_views.xml',
        'views/product_card_views.xml',
        'views/product_page_views.xml',
        'views/shop_views.xml',
        'views/menu.xml',
        'views/categories_home_shop.xml',
        'views/product_template_form_views.xml',
        
        'views/portal_my_details_fields.xml',
        'views/public_category_views.xml',
        'security/ir.model.access.csv',
	],
    'assets': {
        'web.assets_frontend': [
            ('prepend', 'website_sale_custom_destockinfo/static/src/scss/**.scss'),
        ]
    },
    'auto_install': True,
}
