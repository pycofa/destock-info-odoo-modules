# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Web SaaS',
    'category': 'Hidden',
    'license': 'Other proprietary',
    'description': 'Web configuration for SaaS',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'auto_install': [
        'pyper_saas',
        'web',
    ],
    'depends': [
        'pyper_saas',
        'base',
        'web',
    ],
    'data': [
        # Data
        'views/webclient_templates.xml',
    ],
}
