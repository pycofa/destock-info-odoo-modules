# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).


{
    'name': 'Website Buyback request',
    'category': 'Website/Website',
    'license': 'Other proprietary',
    'description': 'Website Buyback request',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'installable': True,
    'depends': [
        # Base
        'website_sale',
    ],
    'data': [
        # Data
        'data/buyback_data.xml',
        
        # Views
        'views/buyback_request_views.xml',
        'views/res_config_settings_views.xml',
        'views/buyback_form.xml',

        # Security
        'security/ir.model.access.csv',
    ],
}
