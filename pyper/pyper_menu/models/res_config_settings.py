# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    menu_prefer_web_icon = fields.Boolean(
        'Prefer web icons of menu items?',
        config_parameter='pyper_menu.provider.preferWebIcon',
    )
