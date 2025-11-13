# -*- coding: utf-8 -*-
{
    'name': 'Signup Email Verification - French UX',
    'version': '1.0.0',
    'category': 'Website',
    'summary': 'French user experience improvements for email signup verification',
    'description': """
French UX Improvements for Signup Email Verification

This module extends the sh_signup_email_approval module to provide:
- Pedagogical French messages for non-technical users
- Explanatory text before signup button
- Renamed button labels (S'inscrire)
- Improved UX flow for French-speaking users

This is an inheritance module that does NOT modify the vendor module directly,
ensuring compatibility with future updates.
    """,
    'author': 'Destock Info',
    'website': 'https://destock.info',
    'depends': ['sh_signup_email_approval'],
    'data': [
        'views/signup_template.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'destockinfo_signup_email_fr/static/src/js/signup_fr_patch.js',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}