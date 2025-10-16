# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Product extend features IT',
    'category': 'Extra Tools',
    'license': 'Other proprietary',
    'description': 'Add ability to extend product information with custom category features around IT',
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
        'pyper_product_extend_features',
    ],
    'data': [
        # Security
        'security/ir.model.access.csv',

        # Views
        'views/product_template_views.xml',
        'views/product_category_views.xml',
        'views/product_operating_system_views.xml',
        'views/product_storage_type_views.xml',
        'views/product_storage_capacity_views.xml',
        'views/product_processor_views.xml',
        'views/product_processor_model_views.xml',
        'views/product_processor_generation_views.xml',
        'views/product_screen_size_views.xml',
        'views/product_graphic_card_views.xml',
        'views/product_screen_quality_views.xml',
        'views/product_networks_views.xml',
        'views/product_video_input_views.xml',
        'views/product_video_output_views.xml',
        
        # Menu
        'views/menu.xml',
    ],
}
