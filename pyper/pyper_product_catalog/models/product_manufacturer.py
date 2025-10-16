# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).
from types import NoneType

from odoo import fields, models


class ProductManufacturer(models.Model):
    _name = 'product.manufacturer'
    _description = 'Product manufacturer'
    _order = "name ASC"
    _inherit = ['image.mixin']

    name = fields.Char(
        string='Name'
    )
