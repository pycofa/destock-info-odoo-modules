# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models

class ProductVideoInput(models.Model):
    _name = 'product.video.input'
    _description = 'Product video input'
    _order = 'sequence ASC'

    sequence = fields.Integer(string='Sequence')

    name = fields.Char(string='Name')
