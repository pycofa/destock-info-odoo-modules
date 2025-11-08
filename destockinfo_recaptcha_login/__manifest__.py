# -*- coding: utf-8 -*-
# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Destockinfo reCAPTCHA Login',
    'category': 'Website',
    'license': 'Other proprietary',
    'description': '''
This module extends google_recaptcha to add reCAPTCHA support on the login page (/web/login).

By default, Odoo's google_recaptcha module only supports:
- Signup page (/web/signup)
- Reset password page (/web/reset_password)

This module adds support for:
- Login page (/web/login)
    ''',
    'summary': 'Add Google reCAPTCHA v3 on login page',
    'version': '1.0.2',
    'author': 'Krafter SAS',
    'maintainer': ['Krafter SAS'],
    'website': 'https://krafter.io',
    'depends': [
        'google_recaptcha',  # Module natif Odoo
        'web',
    ],
    'data': [],
    'assets': {
        'web.assets_frontend': [
            'destockinfo_recaptcha_login/static/src/js/login_recaptcha.js',
            'destockinfo_recaptcha_login/static/src/js/login_recaptcha_start.js',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
