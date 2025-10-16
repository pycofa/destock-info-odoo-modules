# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class ServerActions(models.Model):
    _inherit = 'ir.actions.server'

    icon = fields.Char(
        'Icon'
    )
