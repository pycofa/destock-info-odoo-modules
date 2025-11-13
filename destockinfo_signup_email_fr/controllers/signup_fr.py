# -*- coding: utf-8 -*-
from odoo import http, _
from odoo.addons.sh_signup_email_approval.controllers.outh_otp_verifaction import otp_auth_AuthSignupHome


class SignupFrenchUX(otp_auth_AuthSignupHome):
    """
    Extends the OTP signup controller to provide French-friendly messages.
    Only overrides the success message to make it more pedagogical for non-technical users.
    """
    
    @http.route('/auth/send_otp', type='json', auth='public', methods=['POST'], csrf=False)
    def auth_send_otp(self, email, **kwargs):
        """Override to provide pedagogical French success message"""
        response = super().auth_send_otp(email, **kwargs)
        
        if response.get('success'):
            # Replace with pedagogical message for French users
            response['message'] = _(
                'Un code de vérification vient de vous être envoyé par e-mail. '
                'Consultez votre messagerie (pensez à vérifier vos courriers indésirables) '
                'et saisissez le code ci-dessous pour finaliser votre inscription.'
            )
        
        return response