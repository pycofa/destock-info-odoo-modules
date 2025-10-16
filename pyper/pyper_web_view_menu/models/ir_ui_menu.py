# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class IrUiMenu(models.Model):
    _inherit = 'ir.ui.menu'

    user_id = fields.Many2one(
        'res.users',
        string='User',
        ondelete='cascade',
    )

    view_id = fields.Many2one(
        'ir.views',
        string='Saved view',
        ondelete='cascade',
    )

    def write(self, vals):
        if self.user_id == self.env.user and not self.env.su:
            res = super().sudo().write(vals)
        else:
            res = super().write(vals)

        if self.user_id and self.view_id:
            for partner in self.user_id.partner_id:
                self.env['bus.bus']._sendone(partner, 'user_menu_view_changed', {})

        return res

    def unlink(self):
        partner_id = self.user_id.partner_id
        user_menu_view_changed = bool(self.user_id and self.view_id)

        res = super().unlink()

        if user_menu_view_changed:
            for partner in partner_id:
                self.env['bus.bus']._sendone(partner, 'user_menu_view_changed', {})

        return res
