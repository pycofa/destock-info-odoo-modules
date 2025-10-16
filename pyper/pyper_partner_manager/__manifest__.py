# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Partner Manager',
    'category': 'Hidden/Tools',
    'license': 'Other proprietary',
    'description': 'Override of default sale addon.',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'installable': True,
    'depends': [
        'base',
        'mail',
    ],
    'data': [
        # Views
        'views/res_partner_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'pyper_partner_manager/static/src/scss/style.scss',
        ],
    }
}
