# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class BuybackRequest(models.Model):
    _name = 'buyback.request'
    _description = 'Buyback request'
    _rec_name = 'subject'

    subject = fields.Char(string='Subject')
    name = fields.Char(string='Contact Name')
    phone = fields.Char(string='Phone Number')
    email = fields.Char(string='Email Address')
    content = fields.Text(string='Content')
    attached_file = fields.Binary(string='Attached File')
