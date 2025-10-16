# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import models


class IrUiView(models.Model):
    _inherit = 'ir.ui.view'

    def _render_template(self, template, values=None):
        icp = self.env['ir.config_parameter'].sudo()
        web_app_name = icp.get_param('web.web_app_name', icp._get_web_app_name())

        values.update({'_web_app_name': web_app_name})

        return self.env['ir.qweb']._render(template, values)
