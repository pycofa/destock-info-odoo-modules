# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Website SaaS',
    'category': 'Hidden',
    'license': 'Other proprietary',
    'description': 'Website configuration for SaaS',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'installable': True,
    'auto_install': [
        'pyper_saas',
        'web',
        'website',
    ],
    'depends': [
        'pyper_saas',
        'web',
        'website',
    ],
    'data': [
        'data/rules.xml',
        'views/website_templates.xml',
    ],
}
