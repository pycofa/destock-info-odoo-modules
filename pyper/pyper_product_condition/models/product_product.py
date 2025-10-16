# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models, api

class ProductProduct(models.Model):
    _inherit = 'product.product'

    product_condition_id = fields.Many2one(
        'product.condition',
        'Product Condition',
        compute='_compute_product_condition',
        search=True,
    )

    product_condition_description = fields.Char(
        related='product_condition_id.description',
        string='Product Condition Description',
    )

    @api.depends('product_template_attribute_value_ids')
    def _compute_product_condition(self):
        for product in self:
            product_condition_id = False
            for product_attribute_value in product.product_template_attribute_value_ids.product_attribute_value_id:
                if product_attribute_value.product_condition_id:
                    product_condition_id = product_attribute_value.product_condition_id
                    break

            product.product_condition_id = product_condition_id
