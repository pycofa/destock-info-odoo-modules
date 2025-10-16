# Copyright Krafter SAS <hey@krafter.io>
# Odoo Proprietary License (see LICENSE file).


{
    'name': 'Mass Mailing Product Cards',
    'category': 'Hidden/Tools',
    'license': 'Other proprietary',
    'description': 'This addon allow to add product cards into mailing template !',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'installable': True,
    'application': True,
    'auto_install': [
        'website',
    ],
    'depends': [
        'website',
        'mass_mailing_themes',
    ],
    'data': [
        # Views
        'views/snippets/s_product_container.xml',
        'views/snippet_theme.xml',
        'views/add_product_mailing.xml',
        'views/unsubscribe_link_template.xml',
        
        # Wizard
        'wizard/product_mailing_wizard.xml',
        'security/ir.model.access.csv',
    
    ],
    'assets': {

    }
}
