# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import models
from odoo.tools import file_open

import csv


class IrUiMenu(models.Model):
    _inherit = 'ir.ui.menu'

    def _update_root_icons(self):
        icons = {}

        with file_open('pyper_web_theme_icons/data/menu_icons.csv', 'r') as csv_file:
            for row in csv.DictReader(csv_file):
                icons.update({row['module']: row['font_icon']})

        menus = self.env['ir.ui.menu'].search([('web_icon', '!=', False), ('font_icon', '=', False)])

        for menu in menus:
            addon,icon = menu.web_icon.split(',')

            if menu.web_icon in icons:
                menu.font_icon = icons.get(menu.web_icon)
            elif addon in icons:
                menu.font_icon = icons.get(addon)
