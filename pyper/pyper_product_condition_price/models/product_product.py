# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models, api, _

class ProductProduct(models.Model):
    _inherit = 'product.product'

    sale_price = fields.Float(string='Sale price')
