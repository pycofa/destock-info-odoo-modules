# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class IrUiMenu(models.Model):
    _inherit = 'ir.ui.menu'

    position = fields.Selection(
        selection_add=[
            ('drawer_quick_actions', 'Drawer Quick Actions'),
            ('drawer_footer', 'Drawer Footer'),
        ],
    )
