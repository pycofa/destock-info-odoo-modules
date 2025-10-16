# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    image_url = fields.Char(string='Image URL')
