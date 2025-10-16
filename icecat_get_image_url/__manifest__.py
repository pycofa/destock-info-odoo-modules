# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).


{
    'name': 'Get image url from icecat form',
    'category': 'Website/Website',
    'license': 'Other proprietary',
    'description': 'Get url image from icecat',
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
        
        'pyper_icecat_connector',
    ],
    'data': [
    ],
    'auto_install': ['website_sale', 'pyper_icecat_connector'],
}
