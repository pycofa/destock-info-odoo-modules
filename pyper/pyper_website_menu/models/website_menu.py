# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import api, fields, models


class WebsiteMenu(models.Model):
    _inherit = 'website.menu'

    is_structured_menu = fields.Boolean(
        'Is Structured Menu',
    )

    structured_menu_obfuscator = fields.Boolean(
        'Use obfuscator?',
    )

    parent_is_structured_menu = fields.Boolean(
        'Parent is Structured Menu',
        related='parent_id.is_structured_menu',
    )

    structured_menu_columns = fields.Integer(
        'Number of columns',
        help='Override the number of columns in the structured menu defined in theme',
    )

    font_icon = fields.Char('Font icon')

    font_icon_color = fields.Char('Font icon color')

    description = fields.Char(
        'Description',
        translate=True,
    )

    def write(self, values):
        res = super().write(values)

        for menu in self:
            if menu.is_structured_menu and menu.is_mega_menu:
                menu.is_mega_menu = False

            if menu.is_structured_menu and menu.url:
                menu.url = False

            if not menu.is_structured_menu and menu.structured_menu_columns != 0:
                menu.structured_menu_columns = 0

        return res

    @api.onchange('is_structured_menu')
    def _onchange_is_structured_menu(self):
        for menu in self:
            if menu.is_structured_menu and menu.is_mega_menu:
                menu.is_mega_menu = False

            if menu.is_structured_menu and menu.url:
                menu.url = False

            if not menu.is_structured_menu and menu.structured_menu_columns != 0:
                menu.structured_menu_columns = 0

    def _is_active(self):
        if self.is_structured_menu:
            return False

        return super()._is_active()

    @api.model
    def get_tree(self, website_id, menu_id=None):
        res = super().get_tree(website_id, menu_id)

        def update_tree(node):
            menu = self.browse(node.get('fields').get('id'))
            children = node.get('children', [])

            if menu.is_structured_menu:
                node.get('fields').update({
                    'is_structured_menu': menu.is_structured_menu,
                    'structured_menu_columns': menu.structured_menu_columns,
                    'structured_menu_obfuscator': menu.structured_menu_obfuscator,
                })
            else:
                node.get('fields').update({
                    'parent_is_structured_menu': menu.parent_is_structured_menu,
                    'description': menu.description,
                    'font_icon': menu.font_icon,
                    'font_icon_color': menu.font_icon_color,
                })

            for child in children:
                update_tree(child)

        update_tree(res)

        return res
