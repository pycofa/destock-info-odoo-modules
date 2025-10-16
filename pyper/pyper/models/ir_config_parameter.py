# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import api, models


class IrConfigParameter(models.Model):
    _inherit = 'ir.config_parameter'

    @api.model
    def _get_web_app_name(self):
        return 'Pyper'

    @api.model
    def _get_web_theme_color(self):
        return '#ffffff'

    @api.model
    def _get_web_xicon_path(self):
        return '/pyper/static/img/badge-512x512.svg'

    @api.model
    def _get_web_badge_ios_path(self):
        return '/pyper/static/img/badge-ios.png'

    @api.model
    def _get_offline_icon_path(self):
        return self._get_web_xicon_path().lstrip('/')

    @api.model
    def _get_login_icon_path(self):
        return self._get_web_xicon_path()

    @api.model
    def _get_manifest_icon_sizes(self):
        return {
            '192x192': '/pyper/static/img/badge-192x192.png',
            '512x512': '/pyper/static/img/badge-512x512.png',
        }

    @api.model
    def _get_manifest_background_color(self):
        return '#35bfe5'

    @api.model
    def _get_manifest_theme_color(self):
        return self._get_web_theme_color()

    @api.model
    def _get_shortcuts_module_names(self):
        return []
