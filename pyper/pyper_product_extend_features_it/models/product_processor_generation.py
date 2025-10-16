# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class ProductProcessorGeneration(models.Model):
    _name = 'product.processor.generation'
    _description = 'Product processor generation'
    _order = 'sequence ASC'

    sequence = fields.Integer(string='Sequence')

    name = fields.Char(string='Name')

    model_id = fields.Many2one('product.processor.model')

    logo = fields.Image(
        'Logo',
    )
