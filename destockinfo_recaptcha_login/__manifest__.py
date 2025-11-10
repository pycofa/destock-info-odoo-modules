# -*- coding: utf-8 -*-
# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Destockinfo reCAPTCHA Login',
    'category': 'Website',
    'license': 'Other proprietary',
    'description': '''
This module extends google_recaptcha to add reCAPTCHA support on login and signup pages.

By default, Odoo's google_recaptcha module only supports reset password page.

This module adds support for:
- Login page (/web/login) ✅
- Signup page (/web/signup) ✅
    ''',
    'summary': 'Add Google reCAPTCHA v3 on login and signup pages',
    'version': '1.0.8',
    'author': 'Krafter SAS',
    'maintainer': ['Krafter SAS'],
    'website': 'https://krafter.io',
    'depends': [
        'google_recaptcha',  # Module natif Odoo
        'auth_signup',       # Module natif pour signup
        'web',
    ],
    'data': [],
    'assets': {
        'web.assets_frontend': [
            'destockinfo_recaptcha_login/static/src/js/login_recaptcha.js',
            'destockinfo_recaptcha_login/static/src/js/login_recaptcha_start.js',
            'destockinfo_recaptcha_login/static/src/js/signup_recaptcha.js',
            'destockinfo_recaptcha_login/static/src/js/signup_recaptcha_start.js',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
