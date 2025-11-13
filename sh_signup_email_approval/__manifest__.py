# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    'name': 'Signup Email Verification',
    'author': 'Softhealer Technologies',
    'website': 'http://www.softhealer.com',
    "support": "support@softhealer.com",
    'category': 'Website',
    'summary': "Verify Email Signup E-mail Verification Sign-up Email Confirmation Account Activate By Email Log-in Email Verification Sign-in Mail Verification Signup Verification Log-in Verification Email OTP Verification E-mail Verification Signup Mail Verification Odoo Sign-in Email Verification Sign-in E-mail Verification Sign in Email Verification Sign in E-mail Verification Sign in Mail Verification Log-in E-mail Verification Log-in Mail Verification Log in E-mail Verification Log in Mail Verification Log in Email Verification Signup Email Verification Email verification plugin for website Email verification for user registration Email validation plugin User signup email confirmation Email confirmation module for website Email verification system for signups Email verification for new users Odoo",
    'description': """
Whenever any user sign up, that will pass to the email verification process, the user can log in after email verification. For email, verification users have to verify with the verification code that sent in a user email address. It shows alert if you entered an invalid verification code. Only verified users can access the system.
 Signup Email Verification Odoo
 Verify Email At Signup Module, Email Verification, Email Confirmation On Sign-up, Account Activate By Email, Log-in Email Verification, Sign-in Mail Verification, Signup Verification Odoo
Verify Email At Signup, Email Verification  Module, Sign-up Email Confirmation, Account Activate By Email, Log-in Email Verification, Sign-in Mail Verification, Signup Verification App, Log-in Verification, Email OTP Verification, Odoo Email Verification, Odoo E-mail Verification, Mail OTP Odoo

                    """,
    'version': '0.0.5',
    'depends': [
        'base',
        'auth_signup',
        'portal'
    ],
    'application': True,
    'data': [
        "security/ir.model.access.csv",
        "data/user_mail_template.xml",
        "views/user_signup_template.xml",
        "views/sh_signup_outh_views.xml",
    ],
    'assets': {
        'web.assets_frontend': [
            'sh_signup_email_approval/static/src/js/sh_signup.js',
            'sh_signup_email_approval/static/src/js/scss/sh_signup.scss',
        ],
    },

    'images': ['static/description/background.png', ],
    "license": "OPL-1",
    'auto_install': False,
    'installable': True,
    "price": 35,
    "currency": "EUR"

}
