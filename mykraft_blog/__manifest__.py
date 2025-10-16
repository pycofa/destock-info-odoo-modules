# Copyright Krafter SAS <hey@krafter.io>
# Odoo Proprietary License (see LICENSE file).

{
    'name': 'myKraft blog',
    'category': 'Hidden/Tools',
    'license': 'Other proprietary',
    'description': 'This addon will add menuitems dedicated to website blog',
    'summary': 'This addon will add menuitems dedicated to website blog',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'installable': True,
    'auto_install': [
        'mykraft',
        'website_blog',
    ],
    'depends': [
        'mykraft',
        'website_blog',
    ],
    'data': [
        'views/menu.xml',
    ],
}
