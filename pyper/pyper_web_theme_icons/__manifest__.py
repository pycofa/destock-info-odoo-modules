# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).
{
    'name': 'Web Theme Icons',
    'category': 'Hidden/Tools',
    'license': 'Other proprietary',
    'description': 'Use app icons with Pyper Web Theme',
    'version': '1.0',
    'author': 'Krafter SAS',
    'website': 'https://krafter.io',
    'maintainer': [
        'Krafter SAS',
    ],
    'post_init_hook': 'post_init_hook',
    'auto_install': [
        'pyper_fonts_phosphor',
        'pyper_web_theme',
    ],
    'depends': [
        'base',
        'web',
        'pyper_menu',
        'pyper_fonts_phosphor',
        'pyper_web_theme',
    ],
}
