from odoo import http
from odoo.http import request
from odoo.addons.website.controllers.form import WebsiteForm
import json
import textwrap

class WebsiteFormCustom(WebsiteForm):

    @http.route('/website/form/<string:model_name>', type='http', auth="public", methods=['POST'], website=True, csrf=False)
    def website_form(self, model_name, **kwargs):

        if model_name == 'website.sale.quotation':
            email_to = request.env['ir.config_parameter'].sudo().get_param('website_sale_quotation.email_to_for_quotation')
            email_cc = (request.env['ir.config_parameter'].sudo().get_param('website_sale_quotation.email_cc_for_quotation') or '').split(',')

            if kwargs.get('from_wishlist'):
                product_ids = request.env['product.wishlist'].search([('partner_id', '=', request.env.user.partner_id.id)]).mapped('product_id.product_tmpl_id')
            else:
                product_ids = request.env['product.template'].browse(kwargs['product_ids'])

            content = '''   <p>Nom : {name}</p>
                            <p>Tel : {phone}</p>
                            <p>{description}</p>
                            <p>{description}</p>
                            <p>{product_ids}</p>
                        '''.format(description=kwargs.get('content'),
                                   phone=kwargs.get('phone'), name=kwargs.get('name'), product_ids=product_ids.mapped('name'))

            mail_values = {
                'subject': kwargs.get('subject'),
                'body_html': content,
                'email_to': email_to,
                'email_cc': email_cc,
                'email_from': kwargs.get('email_from'),
            }
            mail = request.env['mail.mail'].sudo().create(mail_values)
            mail.send()

            res = super().website_form(model_name, **kwargs)
            res_id = json.loads(res.data.decode('utf-8'))['id']
            quotation = request.env['website.sale.quotation'].browse(res_id)
            content = textwrap.dedent('''
                            {description}\n
                        ''').format(description=kwargs.get('content'))
            quotation.sudo().write({
                'product_ids': product_ids.ids,
                'content': content
            })

            return res

        return super().website_form(model_name, **kwargs)
