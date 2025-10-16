# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Product condition extend features IT',
    'category': 'Manufacturing/Repair',
    'license': 'Other proprietary',
    'description': 'This addon adds ability to display condition on dedicated views with extends logics.',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'installable': True,
    'auto_install': [
        'pyper_product_condition',
        'pyper_product_extend_features_it',
    ],
    'depends': [
        'pyper_product_condition',
        'pyper_product_extend_features_it',
    ],
    'data': [
        'views/product_template_views.xml',
    ],
}
