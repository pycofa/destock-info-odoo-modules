# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class ProductAttributeValue(models.Model):
    _inherit = 'product.attribute.value'

    product_condition_id = fields.Many2one(
        'product.condition',
    )

    description = fields.Char(
        related='product_condition_id.description',
    )

    condition_type = fields.Selection(
        related='product_condition_id.condition_type',
    )
