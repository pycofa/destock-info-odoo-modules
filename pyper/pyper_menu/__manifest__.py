# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Menu',
    'category': 'Hidden/Tools',
    'license': 'Other proprietary',
    'description': 'Extend Web Interface of menus.',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'post_init_hook': 'post_init_hook',
    'depends': [
        'base',
        'web',
        'pyper',
        'pyper_setup',
    ],
    'data': [
        # Security
        'security/ir.model.access.csv',

        # Data
        'data/ir_ui_menu_category_data.xml',

        # Views
        'views/ir_ui_menu_category_views.xml',
        'views/ir_ui_menu_views.xml',
        'views/res_config_settings_views.xml',
        'views/menu.xml',
    ],
    'assets': {
        'web._assets_primary_variables': [
            'pyper_menu/static/src/**/*.variables.scss',
        ],
        'web.assets_backend': [
            'pyper_menu/static/src/webclient/**/*',
        ],
    },
}
