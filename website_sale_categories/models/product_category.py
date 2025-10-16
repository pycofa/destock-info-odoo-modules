# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = 'product.category'
    

    family_code = fields.Char(string="Family Code")
