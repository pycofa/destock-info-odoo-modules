# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Icecat connector',
    'category': 'Services/Project',
    'license': 'Other proprietary',
    'description': 'Add ability to get product information from Icecat database',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'installable': True,
    'depends': [
        'product',
		'stock',
        'pyper_product_catalog',
    ],
    'data': [
        # Security
        'security/ir.model.access.csv',

        # Wizard
        'wizard/icecat_form.xml',
        'wizard/menu.xml',
    ],
}
