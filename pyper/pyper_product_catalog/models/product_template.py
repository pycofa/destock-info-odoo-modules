# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_manufacturer_id = fields.Many2one(
        'product.manufacturer',
        'Manufacturer',
    )

    product_manufacturer_logo = fields.Image(
        related="product_manufacturer_id.image_1920",
        string='Product Manufacturer Logo',
    )

    ean_upc = fields.Char(
        'EAN/UPC',
    )

    gtin = fields.Char(
        'GTIN',
    )

    part_number_code = fields.Char(
        'Part number',
    )


