# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

import odoo.addons.pyper.controllers.webmanifest as webmanifest


class myKraftWebManifest(webmanifest.WebExtraWebManifest):

    def _get_default_web_app_name(self):
        return 'myKraft'

    def _get_offline_icon_path(self):
        return 'mykraft/static/img/badge-512x512.svg'

    def _get_manifest_icon_sizes(self):
        return {
            '192x192': '/mykraft/static/img/badge-192x192.png',
            '512x512': '/mykraft/static/img/badge-512x512.png',
        }

    def _get_manifest_background_color(self):
        return '#333333'

    def _get_manifest_theme_color(self):
        return '#333333'
