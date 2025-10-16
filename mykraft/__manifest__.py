# Copyright Krafter SAS <hey@krafter.io>
# Odoo Proprietary License (see LICENSE file).




{
    'name': 'myKraft',
    'category': 'Hidden/Tools',
    'license': 'Other proprietary',
    'description': 'This addon will help you design awesome websites !',
    'summary': 'This addon will help you design awesome websites !',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'installable': True,
    'application': True,
    'post_init_hook': 'post_init_hook',
    'auto_install': [
        'web',
    ],
    'depends': [
        'web',
        'mail',
        'base',
        'digest',
        'web',
        'web_editor',
        'http_routing',
        'portal',
        'social_media',
        'auth_signup',
        'mail',
        'google_recaptcha',
        'utm',
        'website',

        # Pyper
        'pyper',
        'pyper_access_rights',
        'pyper_activity',
        'pyper_command_search',
        'pyper_fonts_phosphor',
        'pyper_drawer',
        'pyper_menu',
        'pyper_web_theme',
        'pyper_web_theme_activity',
        'pyper_web_theme_discuss',
        'pyper_web_view',
        'pyper_website_snippets',
    ],
    'data': [
        # Data
        'data/bot.xml',
        'data/groups.xml',

        # Views
        'views/webclient_templates.xml',
        'views/menu.xml',

    ],
    'assets': {
        'web._assets_primary_variables': [
            ('before', 'pyper_web_theme/static/src/scss/primary_variables.scss',
             'mykraft/static/src/scss/primary_variables.scss'),
        ],
        'web.assets_backend': [
            ('prepend', 'mykraft/static/src/font/archivo.scss'),

            ('prepend', 'pyper_fonts_phosphor/static/src/scss/phosphor-regular.scss'),
            ('prepend', 'pyper_fonts_phosphor/static/src/scss/phosphor-light.scss'),
            
            
            'mykraft/static/src/scss/pyper_animate.scss',
            'mykraft/static/src/scss/style_form_sheet_full.scss',
            '/mykraft/static/src/js/cascade_animation.js',
            'mykraft/static/src/scss/style.scss',
            'mykraft/static/src/core/**/*',
            'mykraft/static/src/mail/**/*',
            'mykraft/static/src/search/**/*',
            'mykraft/static/src/views/**/*',
            'mykraft/static/src/webclient/**/*',
        ],

        'web.assets_frontend': [
            "mykraft/static/src/scss/front/style.scss",
            'mykraft/static/src/scss/pyper_animate.scss',
            "mykraft/static/src/scss/style.scss"
        ],
    }
}
