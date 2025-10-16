# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class WebsiteSaleQuotation(models.Model):
    _name = 'website.sale.quotation'
    _description = 'Website sale quotation'
    
    subject = fields.Char(string='Subject')
    name = fields.Char(string='Contact Name')
    phone = fields.Char(string='Phone Number')
    email_from = fields.Char(string='Email Address')
    content = fields.Text(string='Content')
    product_ids = fields.Many2many('product.template', string='Products')
