# Copyright Krafter SAS <hey@krafter.io>
# Odoo Proprietary License (see LICENSE file).

{
    'name': 'myKraft contacts',
    'category': 'Hidden/Tools',
    'license': 'Other proprietary',
    'description': 'This addon will add menuitems dedicated to website contact and marketing management',
    'summary': 'This addon will add menuitems dedicated to website contact and marketing management',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'installable': True,
    'auto_install': [
        'contacts',
        'mass_mailing',
    ],
    'depends': [
        'contacts',
        'mass_mailing',
    ],
    'data': [
        'views/menu.xml',
    ],
}
