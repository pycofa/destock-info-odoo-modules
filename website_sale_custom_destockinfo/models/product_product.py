# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'


    def get_price_list_item(self):
        today = fields.Date.today()
        if len(self.product_tmpl_id.product_variant_ids) == 1:
            return self.env['product.pricelist.item'].search([
                ('product_tmpl_id', '=', self.product_tmpl_id.id),
                ('date_start', '<=', today),
                ('date_end', '>=', today),
                ('min_quantity', '<=', self.qty_available)
            ], limit=1)
        else:
            return self.env['product.pricelist.item'].search([
                ('product_id', '=', self.id),
                ('date_start', '<=', today),
                ('date_end', '>=', today),
                ('min_quantity', '<=', self.qty_available)
            ], limit=1)
