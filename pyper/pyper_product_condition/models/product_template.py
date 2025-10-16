# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    child_ids = fields.One2many(
        'product.product',
        'product_tmpl_id',
        'Variants',
    )

    count_child_ids = fields.Integer(
        'Total child ids',
        compute='_compute_count_child_ids',
    )

    @api.depends('child_ids')
    def _compute_count_child_ids(self):
        for product in self:
            product.count_child_ids = len(product.child_ids)
