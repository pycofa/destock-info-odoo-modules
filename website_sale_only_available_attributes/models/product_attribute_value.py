# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import api, models, fields


class ProductAttributeValue(models.Model):
    _inherit = 'product.attribute.value'

    pav_available = fields.Boolean(compute='_compute_attribute_value')
    pav_visible_shop = fields.Boolean('Attribute visible', default=True)

    @api.depends('pav_attribute_line_ids.product_tmpl_id.product_variant_ids')
    def _compute_attribute_value(self):
        for rec in self.sudo():
            rec.pav_available = False
            for var in rec.pav_attribute_line_ids.sudo().mapped('product_tmpl_id.product_variant_ids'):
                if var.qty_available > 0:
                    var.sudo().product_template_attribute_value_ids.mapped(
                        'product_attribute_value_id'
                    ).sudo().write({'pav_available': True})
