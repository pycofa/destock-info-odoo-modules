# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Open AI Connector',
    'category': 'Hidden/Tools',
    'license': 'Other proprietary',
    'description': 'Add ability to use Open AI API',
    'summary': 'Add ability to use Open AI API',
    'version': '1.0',
    'author': 'Krafter SAS',
    'installable': True,
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'external_dependencies': {
        'python': [
            'openai',
        ]
    },
    'depends': [
        'base',
        'web',
    ],
    'data': [
        # Views
        'views/res_config_settings_views.xml',
    ],
    'assets': {
    },
}
