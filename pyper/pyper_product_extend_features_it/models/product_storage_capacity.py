# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class ProductStorageCapacity(models.Model):
    _name = 'product.storage.capacity'
    _description = 'Product storage capacity'
    _order = 'sequence ASC'

    sequence = fields.Integer(string='Sequence')

    name = fields.Char(string='Name')
