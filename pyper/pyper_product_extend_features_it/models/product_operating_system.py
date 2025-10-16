# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models

class ProductOperatingSystem(models.Model):
    _name = 'product.operating.system'
    _description = 'Product Operating System'
    _order = 'name DESC'

    name = fields.Char(string='Name')

    logo = fields.Image('Logo')

