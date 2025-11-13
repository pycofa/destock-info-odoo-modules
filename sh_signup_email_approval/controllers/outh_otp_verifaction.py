# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
import werkzeug
import logging
from odoo import http, _
from odoo.http import request
import random
from odoo.addons.auth_signup.models.res_users import SignupError
from odoo.exceptions import UserError
from werkzeug.urls import url_encode
from odoo.addons.auth_signup.controllers.main import AuthSignupHome

_logger = logging.getLogger(__name__)


class otp_auth_AuthSignupHome(AuthSignupHome):
    @http.route('/auth/send_otp', type='json', auth='public', methods=['POST'], csrf=False)
    def auth_send_otp(self, email, **kwargs):
        user = request.env['res.users'].sudo().search(
            [('login', '=', email)], limit=1)

        if not user:
            otp = str(random.randint(100000, 999999))
            otp_verification_id = request.env['sh.signup.outh'].sudo().search([
                ("email", "=", email)])

            if otp_verification_id:
                otp_verification_id.sudo().write({
                    'name': otp,
                })
            else:
                otp_verification_id = request.env['sh.signup.outh'].sudo().create({
                    'name': otp,
                    'email': email,
                    'company_id': request.env.company.id,
                    'partner_id': user.partner_id.id if user else False
                })

            template = request.env.ref(
                'sh_signup_email_approval.sh_user_mail_template')
            if template:
                companyEmail = request.env.company
                template.sudo().send_mail(otp_verification_id.id, force_send=True,
                                          email_values={'email_to': email, 'email_from': companyEmail.email})
            return {'success': True, 'message': 'OTP sent successfully to your email.'}
        return {'success': False, 'message': 'Email not found in the system.'}

    @http.route('/auth/verify_otp', type='json', auth='public', methods=['POST'], csrf=False)
    def auth_verify_otp(self, email, otp, **kw):
        otp = otp
        login = email

        otp_data = request.env['sh.signup.outh'].sudo().search([
            ("email", "=", login),
            ("name", "=", otp)
        ])

        if otp_data:
            return {'success': True, 'message': 'OTP verified successfully.'}
        
        return {'success': False, 'message': 'Invalid OTP.'}


    @http.route('/web/signup', type='http', auth='public', website=True, sitemap=False)
    def web_auth_signup(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()
    
        if not qcontext.get('token') and not qcontext.get('signup_enabled'):
            raise werkzeug.exceptions.NotFound()

        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                self.do_signup(qcontext)
                # Send an account creation confirmation email
                User = request.env['res.users']
                user_sudo = User.sudo().search(
                    User._get_login_domain(qcontext.get('login')), order=User._get_login_order(), limit=1
                )
                template = request.env.ref('auth_signup.mail_template_user_signup_account_created', raise_if_not_found=False)
                if user_sudo and template:
                    template.sudo().send_mail(user_sudo.id, force_send=True)
                return self.web_login(*args, **kw)
            except UserError as e:
                qcontext['error'] = e.args[0]
            except (SignupError, AssertionError) as e:
                if request.env["res.users"].sudo().search([("login", "=", qcontext.get("login"))]):
                    qcontext["error"] = _("Another user is already registered using this email address.")
                else:
                    _logger.error("%s", e)
                    qcontext['error'] = _("Could not create a new account.")

        elif 'signup_email' in qcontext:
            user = request.env['res.users'].sudo().search([('email', '=', qcontext.get('signup_email')), ('state', '!=', 'new')], limit=1)
            if user:
                return request.redirect('/web/login?%s' % url_encode({'login': user.login, 'redirect': '/web'}))

        response = request.render('auth_signup.signup', qcontext)
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['Content-Security-Policy'] = "frame-ancestors 'self'"
        return response