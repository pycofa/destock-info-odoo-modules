# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models

class ProductGraphicCard(models.Model):
    _name = 'product.graphic.card'
    _description = 'Product graphic card'
    _order = 'sequence ASC'

    sequence = fields.Integer(string='Sequence')

    name = fields.Char(string='Name')
