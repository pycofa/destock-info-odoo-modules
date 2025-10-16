# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import models


class IcecatForm(models.TransientModel):
    _inherit = 'icecat.form'


    def action_icecat_api_call(self):
        self.ensure_one()
        res = super().action_icecat_api_call()
        res_model = res.get('res_model')
        res_id = res.get('res_id')
        image_url = res.get('image_url')
        
        if image_url:
            product = self.env[res_model].search([('id', '=', res_id)])
            if product:
                product.image_url = image_url

        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'res_model': res_model,
            'view_mode': 'form',
            'res_id': res_id,
            'target': 'current',
        }
