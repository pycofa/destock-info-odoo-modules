# Copyright Krafter SAS <hey@krafter.io>
# Odoo Proprietary License (see LICENSE file).

{
    'name': 'Destock Info',
    'category': 'Hidden/Tools',
    'license': 'Other proprietary',
    'description': 'Install all addons required for Destock Info project.',
    'summary': 'Install all addons required for Destock Info.',
    'version': '17.0.0.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'installable': True,
    'application': True,
    'depends': [
        # Base
        'base',
        'base_setup',

        # Pyper
        'pyper_fonts_phosphor',
        'pyper_saas',
        'pyper_web_theme_activity',
        'pyper_web_theme',
        'pyper_contact',
        'pyper_partner_manager',
        'pyper_product_condition',
        'pyper_product_extend_features',
        'pyper_product_extend_features_it',

        # Custom
        'mykraft',
    ],
    'data': [
        # Data
        'data/bot.xml',

        # Views
        'views/menu.xml',
    ],
}
