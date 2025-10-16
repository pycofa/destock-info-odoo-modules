# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Control Panel',
    'category': 'Hidden/Tools',
    'license': 'Other proprietary',
    'description': 'Extend Web Interface with innovative control panel.',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'depends': [
        'base',
        'web',
    ],
    'assets': {
        'web.assets_backend': [
            ('after', 'web/static/src/search/control_panel/control_panel.xml','pyper_control_panel/static/src/search/control_panel/control_panel.xml'),
            ('after', 'web/static/src/search/control_panel/control_panel.scss','pyper_control_panel/static/src/search/control_panel/control_panel.scss'),
            ('after', 'web/static/src/search/cog_menu/cog_menu.xml', 'pyper_control_panel/static/src/search/control_panel/cog_menu.xml'),
            ('after', 'web/static/src/views/form/form_status_indicator/form_status_indicator.xml', 'pyper_control_panel/static/src/views/form/form_status_indicator/form_status_indicator.xml'),
            ('after', 'web/static/src/views/form/form_controller.xml', 'pyper_control_panel/static/src/views/form/form_controller.xml'),
        ],
    },
}
