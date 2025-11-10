# -*- coding: utf-8 -*-
# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

import logging
from odoo import http
from odoo.http import request
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class DestockinfoAuthSignupHome(AuthSignupHome):
    """
    Extend the native signup controller to add reCAPTCHA validation.

    This controller intercepts the /web/signup POST request and validates
    the reCAPTCHA token before allowing the signup to proceed.
    """

    @http.route('/web/signup', type='http', auth='public', website=True, sitemap=False)
    def web_auth_signup(self, *args, **kw):
        """
        Override the native signup route to add reCAPTCHA validation.

        The reCAPTCHA token is sent from the frontend as 'recaptcha_token_response'
        and validated using Odoo's native _verify_request_recaptcha_token method.
        """
        # Only validate reCAPTCHA on POST (actual signup submission)
        if request.httprequest.method == 'POST':
            try:
                # Verify reCAPTCHA token using Odoo's native method
                # This will raise ValidationError if token is invalid or score is too low
                _logger.info('[Destock reCAPTCHA] Validating reCAPTCHA token for signup...')
                request.env['ir.http']._verify_request_recaptcha_token('signup')
                _logger.info('[Destock reCAPTCHA] reCAPTCHA validation passed for signup')
            except ValidationError as e:
                # reCAPTCHA validation failed
                _logger.warning('[Destock reCAPTCHA] reCAPTCHA validation failed for signup: %s', str(e))

                # Get the error message and pass it to the template
                qcontext = self.get_auth_signup_qcontext()
                qcontext['error'] = str(e)
                response = request.render('auth_signup.signup', qcontext)
                response.headers['X-Frame-Options'] = 'SAMEORIGIN'
                response.headers['Content-Security-Policy'] = "frame-ancestors 'self'"
                return response

        # If validation passed (or GET request), proceed with normal signup flow
        return super(DestockinfoAuthSignupHome, self).web_auth_signup(*args, **kw)
