# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models

class ProductCondition(models.Model):
    _name = 'product.condition'
    _description = 'Product condition'

    sequence = fields.Integer(
        string='Sequence',
    )

    name = fields.Char(
        string='Name',
        translate=True,
    )

    description = fields.Char(
        string='Description',
        translate=True,
    )

    color = fields.Char(
        string='Color',
    )

    condition_type = fields.Selection(
        [
            ('new', 'New'),
            ('used', 'Used'),
            ('to_define', 'To define'),
            ('not_working', 'Not working'),
        ],
        'Type',
    )
