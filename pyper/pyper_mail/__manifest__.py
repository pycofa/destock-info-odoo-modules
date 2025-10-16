# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).
{
    'name': 'Mail Extra',
    'category': 'Hidden/Tools',
    'license': 'Other proprietary',
    'description': 'Add extra information',
    'version': '1.0',
    'author': 'Krafter SAS',
    'website': 'https://krafter.io',
    'maintainer': [
        'Krafter SAS',
    ],
    'installable': True,
    'depends': [
        'base',
        'web',
        'mail',
    ],
    'assets': {
        'web.assets_backend': [
            'pyper_mail/static/src/core/**/*',
        ],
    },
}
