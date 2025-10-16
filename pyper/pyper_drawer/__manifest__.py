# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Drawer',
    'category': 'Hidden/Tools',
    'license': 'Other proprietary',
    'description': 'Extend Web Interface with drawer.',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
    'depends': [
        'base',
        'web',
        'pyper',
        'pyper_menu',
        'pyper_setup',
    ],
    'data': [
        'views/ir_ui_menu_views.xml',
        'views/res_config_settings_views.xml',
    ],
    'assets': {
        'web._assets_primary_variables': [
            'pyper_drawer/static/src/**/*.variables.scss',
        ],
        'web.assets_backend': [
            'pyper_drawer/static/src/webclient/**/*',
        ],
    },
}
