# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import models


class IrModuleModule(models.Model):
    _inherit = 'ir.module.module'

    def _button_immediate_function(self, function):
        res = super()._button_immediate_function(function)
        self.env['ir.ui.menu'].sudo()._update_root_icons()

        return res
