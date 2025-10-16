# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).
{
    'name': 'Web Theme Command Search',
    'category': 'Hidden/Tools',
    'license': 'Other proprietary',
    'description': 'Make compatible Command Search with Pyper Web Theme',
    'version': '1.0',
    'author': 'Krafter SAS',
    'website': 'https://krafter.io',
    'maintainer': [
        'Krafter SAS',
    ],
    'auto_install': [
        'pyper_command_search',
        'pyper_web_theme',
    ],
    'depends': [
        'base',
        'web',
        'pyper_command_search',
        'pyper_web_theme',
    ],
    'assets': {
        'web.assets_backend': [
            'pyper_web_theme_command_search/static/src/webclient/**/*',
        ],
    },
}
