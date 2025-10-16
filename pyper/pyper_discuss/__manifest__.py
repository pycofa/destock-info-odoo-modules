# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Discuss Extra',
    'category': 'Productivity/Discuss',
    'license': 'Other proprietary',
    'description': 'Split Chatter and Notification center',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'installable': True,
    'depends': [
        'web',
        'mail',
    ],
    'data': [
        'views/discuss_channel_views.xml',
    ],
    'assets': {
        'web.assets_backend': {
            'pyper_discuss/static/src/core/**/*',
            'pyper_discuss/static/src/discuss/**/*',
        },
    },
}
