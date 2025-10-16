# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import api, models, fields


class ProductTemplateAttributeValue(models.Model):
    _inherit = 'product.template.attribute.value'

    def _only_active(self):
        res = super()._only_active()
        av = self._only_available(res)
        if not av:
            av = res
        return av

    def _only_available(self, res):
        variants = res.product_tmpl_id.product_variant_ids
        ptav_available = variants.product_tmpl_id.product_variant_ids.filtered(lambda ptav: ptav.qty_available > 0)
        av = ptav_available.product_template_attribute_value_ids
        return av