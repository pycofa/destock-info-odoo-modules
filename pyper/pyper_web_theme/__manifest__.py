# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).
{
    'name': 'Web Theme',
    'category': 'Hidden/Tools',
    'license': 'Other proprietary',
    'description': 'Add pyper web theme with clean back office theme',
    'version': '1.0',
    'author': 'Krafter SAS',
    'website': 'https://krafter.io',
    'maintainer': [
        'Krafter SAS',
    ],
    'installable': True,
    'application': False,
    'depends': [
        'base',
        'base_setup',
        'web',
        'pyper',
        'pyper_fonts_phosphor',
        'pyper_setup',
    ],
    'data': [
        'views/res_config_settings_views.xml',
        'views/res_partner_views.xml',
    ],
    'assets': {
        'web._assets_primary_variables': [
            ('before', 'web/static/src/scss/primary_variables.scss', 'pyper_web_theme/static/src/scss/primary_variables.scss'),
            ('before', 'web/static/src/**/*.variables.scss', 'pyper_web_theme/static/src/**/*.variables.scss'),
        ],
        'web._assets_secondary_variables': [
            ('before', 'web/static/src/scss/secondary_variables.scss', 'pyper_web_theme/static/src/scss/secondary_variables.scss'),
        ],
        'web._assets_frontend_helpers': [
            ('prepend', 'pyper_web_theme/static/src/scss/bootstrap_overridden.scss'),
        ],
        'web._assets_backend_helpers': [
            ('before', 'web/static/src/scss/bootstrap_overridden.scss', 'pyper_web_theme/static/src/scss/bootstrap_overridden.scss'),
        ],
        'web.assets_frontend': [
            'pyper_web_theme/static/src/scss/style.scss',
        ],
        'web.assets_backend': [
            ('prepend', 'pyper_fonts_phosphor/static/src/scss/phosphor-regular.scss'),
            ('prepend', 'pyper_fonts_phosphor/static/src/scss/phosphor-light.scss'),
            ('prepend', 'pyper_fonts_phosphor/static/src/scss/phosphor-fill.scss'),
            ('after', 'web/static/src/search/search_bar/search_bar.xml', 'pyper_web_theme/static/src/search/search_bar/search_bar.xml'),
            ('after', 'web/static/src/scss/utilities_custom.scss', 'pyper_web_theme/static/src/utilities/**/*'),
            'pyper_web_theme/static/src/scss/style.scss',
            'pyper_web_theme/static/src/legacy/**/*',
            'pyper_web_theme/static/src/core/**/*',
            'pyper_web_theme/static/src/search/control_panel/**/*',
            'pyper_web_theme/static/src/views/**/*',
            'pyper_web_theme/static/src/webclient/**/*',
        ],
    },
}
