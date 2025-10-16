# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).
{
    'name': 'Web Theme Activity',
    'category': 'Hidden/Tools',
    'license': 'Other proprietary',
    'description': '[DEPRECATED] Add activity theme for Pyper Web Theme',
    'version': '1.0',
    'author': 'Krafter SAS',
    'website': 'https://krafter.io',
    'maintainer': [
        'Krafter SAS',
    ],
    'installable': True,
    'application': False,
    'auto_install': [
        'mail',
        'pyper_web_theme',
    ],
    'depends': [
        'web',
        'mail',
        'pyper_web_theme',
        'pyper_web_theme_mail',
    ],
}
