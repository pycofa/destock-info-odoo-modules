# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).
{
    'name': 'Website Menu',
    'category': 'Hidden/Tools',
    'license': 'Other proprietary',
    'description': 'Use menu items to build structured mega menu for website',
    'version': '1.0',
    'author': 'Krafter SAS',
    'installable': True,
    'application': False,
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'depends': [
        'web',
        'website',
    ],
    'data': [
        'views/website_menu_views.xml',
        'views/website_templates.xml',
    ],
    'assets': {
        'web._assets_bootstrap_frontend': [
            'pyper_website_menu/static/src/views/**/*.variables.scss'
        ],

        'website.assets_editor': [
            'pyper_website_menu/static/src/components/dialog/**/*',
        ],

        'web.assets_frontend': [
            'pyper_website_menu/static/src/views/structured_menu/**/*',
            'pyper_website_menu/static/src/libs/bootstrap/**/*',
        ],
    },
}
