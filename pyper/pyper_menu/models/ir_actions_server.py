# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class ServerActions(models.Model):
    _inherit = 'ir.actions.server'

    font_icon = fields.Char('Font icon')

    font_icon_color = fields.Char('Font icon color')
