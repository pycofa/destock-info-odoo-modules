# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Destockinfo Website',
    'category': 'Theme/Krafter',
    'license': 'Other proprietary',
    'description': 'This addon adds necessary elements for Destockinfo website',
    'summary': 'This addon adds necessary elements for Destockinfo website',
    'version': '1.1.0',  # MINOR: New feature - password toggle button
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'application': True,
    'website': 'https://krafter.io',
    'depends': [
        'pyper_fonts_phosphor',
        'website',
        'mass_mailing',
        'web',
        'pyper_website_menu',
        'auth_signup',  # For signup template inheritance
        'portal',  # For account security page inheritance
    ],
    'data': [
        # Views
        'views/portal_views.xml',
        'views/auth_templates.xml',  # Password toggle for login/signup

        'views/website_templates.xml',
        'views/snippet_section.xml',
        'views/snippets/home_hero.xml',
        'views/snippets/s_four_columns_title_text.xml',
        'views/snippets/right_image_simple_text.xml',
        'views/snippets/three_columns_card_title_text.xml',
        'views/snippets/hero_section_contact.xml',
        'views/snippets/cta_section.xml',
        'views/snippets/home_video.xml',
    ],
    'assets': {
        'web._assets_bootstrap_frontend': [
            ('prepend', '/destockinfo_website/static/src/scss/front/website_primary_variables.scss'),
        ],

        'web._assets_secondary_variables': [
            ('prepend', 'destockinfo_website/static/src/scss/front/colors.scss'),
            ('prepend', 'destockinfo_website/static/src/scss/front/secondary_variables.scss'),
        ],

        'web._assets_frontend_helpers': [
            ('prepend', 'pyper_fonts_phosphor/static/src/scss/phosphor-regular.scss'),
            ('prepend', 'pyper_fonts_phosphor/static/src/scss/phosphor-fill.scss'),
            ('prepend', '/destockinfo_website/static/src/scss/front/bootstrap_overriden.scss'),
            ('prepend', '/destockinfo_website/static/src/scss/front/snippets.scss'),
        ],

        'web.assets_frontend': [
            ('prepend', 'destockinfo_website/static/src/font/PlusJakartaSans.scss'),
            '/destockinfo_website/static/src/scss/front/style.scss',
            '/destockinfo_website/static/src/scss/password_toggle.scss',  # Password toggle styles
            '/destockinfo_website/static/src/scss/password_meter_override.scss',  # Fix meter overlap on /my/security
            '/destockinfo_website/static/src/js/front.js',
            '/destockinfo_website/static/src/js/password_toggle.js',  # Password toggle logic
        ],

        'web.assets_frontend_lazy': [
            '/destockinfo_website/static/src/js/front.js',
        ],

        'web.assets_frontend_minimal': [
            '/destockinfo_website/static/src/js/front.js',
        ]
    },
}
