# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class ProductProcessor(models.Model):
    _name = 'product.processor'
    _description = 'Product processor'
    _order = 'sequence ASC'

    sequence = fields.Integer(string='Sequence')

    name = fields.Char(string='Name')

    generation_id = fields.Many2one('product.processor.generation')
