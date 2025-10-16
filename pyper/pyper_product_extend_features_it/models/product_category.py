# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductCategory(models.Model):
    _inherit = 'product.category'

    product_pattern = fields.Selection(
        [
            ('none', 'None'),
            ('all_in_one', 'All-in-one'),
            ('desktop_computer', 'Desktop Computer'),
            ('docking_station', 'Docking station'),
            ('laptop_computer', 'Laptop computer'),
            ('printer', 'Printer'),
            ('projector', 'Projector'),
            ('screen', 'Screen'),
            ('server', 'Server'),
            ('smartphone', 'Smartphone'),
            ('switch', 'Switch'),
            ('tablet', 'Tablet'),
        ]
    )
