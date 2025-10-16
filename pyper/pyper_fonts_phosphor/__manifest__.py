# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Fonts Phosphor',
    'category': 'Hidden/Tools',
    'license': 'Other proprietary',
    'description': 'Phosphor fonts.',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'installable': True,
    'depends': [
        'base_setup',
        'web',
    ],
    'assets': {
        'web.assets_backend': [
            ('prepend', 'pyper_fonts_phosphor/static/src/scss/phosphor-regular.scss'),
        ],
    }
}
