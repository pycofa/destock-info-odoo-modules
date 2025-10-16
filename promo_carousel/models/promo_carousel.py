# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class PromoCarousel(models.Model):
    _name = 'promo.carousel'
    _description = 'Promo carousel displayed on shop\'s carousel'

    name = fields.Char(string='Name')
    image = fields.Image('Image promo')
    activate =  fields.Boolean(string='Activate')
    product_tmpl_id = fields.Many2one('product.template', string='Product')
