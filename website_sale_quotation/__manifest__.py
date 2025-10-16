# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).


{
    'name': 'Website sale quotation',
    'category': 'Website/Website',
    'license': 'Other proprietary',
    'description': 'Website sale quotation',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'installable': True,
    'depends': [
        'website_sale_disable_cart'
    ],
    'data': [
        # Views
        'views/quotation_form.xml',
        'views/config_settings_views.xml',
        'views/website_sale_quotation_views.xml',
        
        # Security
        'security/ir.model.access.csv',
        
        # Data
        'data/website_sale_quotation.xml',
    ],
    'auto_install': True,
}
