# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import api, fields, models, Command


class IrViews(models.Model):
    _inherit = 'ir.views'

    menu_ids = fields.One2many(
        'ir.ui.menu',
        'view_id',
        string='Menu item',
    )

    display_counter = fields.Boolean(
        'Display counter',
        default=True,
        help='Allow to display a counter on menu item when view is bookmarked',
    )

    bookmarked = fields.Boolean(
        string='Bookmarked',
        compute='_compute_bookmarked',
    )

    def write(self, vals):
        res = super().write(vals)
        self._sync_ir_ui_menu()

        return res

    def unlink(self):
        sudo = self.sudo()
        sudo.menu_ids.sudo().unlink()

        return super(IrViews, sudo).unlink()

    @api.model
    def get_menu_vals(self, sync = False):
        self.ensure_one()
        action = self.ir_action_id.sudo()

        vals = {
            'name': self.name,
            'action': str(action.type) + ',' + str(action.id),
            'display_counter': self.display_counter,
            'category_id': self.env.ref('pyper_web_view_menu.menu_category_shared_views').id
                if self.shared
                else self.env.ref('pyper_web_view_menu.menu_category_my_views').id,
            'view_id': self.id,
        }

        if not sync:
            vals.update({
                'user_id': self.env.user.id,
            })

        return vals

    def bookmark(self, font_icon = False):
        for rec in self:
            if not rec.menu_ids:
                menu = self.env['ir.ui.menu'].sudo().create({
                    **rec.get_menu_vals(),
                    'font_icon': font_icon,
                })
                rec.menu_ids = [Command.link(menu.id)]

    def unbookmark(self):
        for rec in self:
            rec.menu_ids.sudo().unlink()

    def _sync_ir_ui_menu(self):
        for rec in self:
            if rec.sudo().menu_ids:
                rec.sudo().menu_ids.write(rec.get_menu_vals(True))

    @api.depends('menu_ids')
    def _compute_bookmarked(self):
        menus = self.menu_ids.sudo().search_read(
            [('user_id', '=', self.env.user.id), ('view_id', 'in', self.ids)],
            ['id', 'view_id']
        )

        map_views = {}

        for menu in menus:
            map_views.update({menu.get('view_id')[0]: menu.get('id')})

        menu_ids = map_views.keys()

        for rec in self:
            rec.bookmarked = rec.id in menu_ids
