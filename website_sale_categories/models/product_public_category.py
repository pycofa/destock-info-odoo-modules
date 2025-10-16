# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class ProductPublicCategory(models.Model):
    _inherit = 'product.public.category'

    categ_filter_visible_in_shop = fields.Boolean('Filter visible in shop', default=True)
    
    shared_category_in_shop = fields.Boolean('Shared category', default=False)
