# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import api, fields, models
import requests
import base64

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    rembg_api_key = fields.Char(
        string='Remove Background API Key',
        compute='_compute_rembg_api_key',
        store=False,
    )
    
    def _compute_rembg_api_key(self):
        for record in self:
            record.rembg_api_key = self.env['ir.config_parameter'].sudo().get_param('remove_image_bg.rembg_api_key')

    
    def action_remove_background(self):
        for rec in self:
            if rec.image_url:
                response = requests.get(rec.image_url)

                if rec.rembg_api_key:
                    response = requests.post(
                        'https://api.remove.bg/v1.0/removebg',
                        files={'image_file': response.content},
                        data={'size': 'auto'},
                        headers={'X-Api-Key': rec.rembg_api_key},
                    )
                    if response.status_code == requests.codes.ok:
                        rec.image_1920 = base64.b64encode(response.content)
                    else:
                        print("Error:", response.status_code, response.text)
                else:
                    print('No API key configured')
