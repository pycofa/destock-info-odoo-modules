# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models

class ProductScreenQuality(models.Model):
    _name = 'product.screen.quality'
    _description = 'Product screen quality'
    _order = 'sequence ASC'

    sequence = fields.Integer(string='Sequence')

    name = fields.Char(string='Name')

    logo = fields.Image(
        'Logo',
    )