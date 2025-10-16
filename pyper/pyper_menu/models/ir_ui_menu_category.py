# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class IrUiMenuCategory(models.Model):
    _name = 'ir.ui.menu.category'
    _description = 'Menu category'
    _order = 'sequence asc, id asc'

    name = fields.Char(
        'Name',
        required=True,
        translate=True,
    )

    sequence = fields.Integer(
        'Sequence',
        default=100,
    )

    font_icon = fields.Char('Font icon')

    font_icon_color = fields.Char('Font icon color')

    ir_action_id = fields.Many2one(
        'ir.actions.act_window',
        string='Action',
        ondelete='set null',
    )
