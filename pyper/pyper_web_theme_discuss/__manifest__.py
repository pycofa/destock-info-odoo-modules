# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).
{
    'name': 'Web Theme Discuss',
    'category': 'Hidden/Tools',
    'license': 'Other proprietary',
    'description': 'Make compatible Discuss Extra with Pyper Web Theme',
    'version': '1.0',
    'author': 'Krafter SAS',
    'website': 'https://krafter.io',
    'maintainer': [
        'Krafter SAS',
    ],
    'auto_install': [
        'pyper_discuss',
        'pyper_web_theme',
    ],
    'depends': [
        'base',
        'web',
        'pyper_discuss',
        'pyper_web_theme',
    ],
    'assets': {
        'web.assets_backend': [
            'pyper_web_theme_discuss/static/src/webclient/**/*',
        ],
    },
}
