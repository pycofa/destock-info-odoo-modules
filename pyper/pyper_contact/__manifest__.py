# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Contact',
    'category': 'Hidden/Tools',
    'license': 'Other proprietary',
    'description': 'Addon dedicated to contact management',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'installable': True,
    'depends': [
        'contacts',
    ],
    'data': [
        # Views
        'views/res_partner_views.xml',
        'views/menu.xml',
    ],
}
