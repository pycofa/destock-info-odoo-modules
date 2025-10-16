
from odoo import http
from odoo.http import request
from odoo.addons.website.controllers.form import WebsiteForm
import base64


class WebsiteFormCustom(WebsiteForm):

    @http.route('/website/form/<string:model_name>', type='http', auth="public", methods=['POST'], website=True, csrf=False)
    def website_form(self, model_name, **kwargs):
        res = super().website_form(model_name, **kwargs)

        if model_name == 'buyback.request':
            attachment = None

            file = kwargs.get('attached_file[0][0]')
            if file:
                attachment = request.env['ir.attachment'].sudo().create({
                    'name': file.filename,
                    'datas': base64.b64encode(file.read()),
                    'res_model': 'buyback.request',
                    'res_id': 0,
                    'type': 'binary',
                    'mimetype': file.content_type,
                })

            email_to = request.env['ir.config_parameter'].sudo().get_param('website_buyback_request.email_to')
            email_cc = (request.env['ir.config_parameter'].sudo().get_param('website_buyback_request.email_cc') or '').split(',')

            content =  ''' <p>{content}</p>
                <p>Nom : {name}</p>
                <p>Tel : {phone}</p>
            '''.format(content=kwargs.get('content'), phone=kwargs.get('phone'), name=kwargs.get('name'))

            mail_values = {
                'subject': kwargs.get('subject'),
                'body_html': content,
                'email_to': email_to,
                'email_cc': email_cc,
                'email_from': kwargs.get('email'),
                'attachment_ids': [(4, attachment.id)] if attachment else [],
            }
            mail = request.env['mail.mail'].sudo().create(mail_values)
            mail.send()

        return res
