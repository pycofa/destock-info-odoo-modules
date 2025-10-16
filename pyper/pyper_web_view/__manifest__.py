# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).
{
    'name': 'Web View',
    'category': 'Hidden/Tools',
    'license': 'Other proprietary',
    'description': 'Save manage and share custom views',
    'version': '1.0',
    'author': 'Krafter SAS',
    'website': 'https://krafter.io',
    'maintainer': [
        'Krafter SAS',
    ],
    'installable': True,
    'application': False,
    'depends': [
        'base',
        'web',
    ],
    'data': [
        # Security
        'security/ir.model.access.csv',
        'security/ir_views_security.xml',

        # Views
        'views/ir_views_views.xml',
        'views/menu.xml',
    ],
    'assets': {
        'web._assets_primary_variables': [
            ('before', 'web/static/src/**/*.variables.scss', 'pyper_web_view/static/src/**/*.variables.scss'),
        ],

        'web.assets_backend': {
            'pyper_web_view/static/src/search/**/*',
        },
    },
}
