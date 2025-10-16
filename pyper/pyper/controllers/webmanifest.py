# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

import base64
import json
import mimetypes

import odoo.addons.web.controllers.webmanifest as webmanifest

from odoo import http
from odoo.exceptions import AccessError
from odoo.http import request
from odoo.tools import ustr, file_open


class WebExtraWebManifest(webmanifest.WebManifest):

    def _get_default_web_app_name(self):
        return request.env['ir.config_parameter'].sudo()._get_web_app_name()

    def _get_offline_icon_path(self):
        return request.env['ir.config_parameter'].sudo()._get_offline_icon_path()

    def _get_manifest_icon_sizes(self):
        return request.env['ir.config_parameter'].sudo()._get_manifest_icon_sizes()

    def _get_manifest_background_color(self):
        return request.env['ir.config_parameter'].sudo()._get_manifest_background_color()

    def _get_manifest_theme_color(self):
        return request.env['ir.config_parameter'].sudo()._get_manifest_theme_color()

    def _get_shortcuts_module_names(self):
        return request.env['ir.config_parameter'].sudo()._get_shortcuts_module_names()

    def _get_shortcuts(self):
        module_names = self._get_shortcuts_module_names()

        try:
            module_ids = request.env['ir.module.module'].search([
                ('state', '=', 'installed'), ('name', 'in', module_names),
            ]).sorted(key=lambda r: module_names.index(r["name"]))
        except AccessError:
            return []

        menu_roots = request.env['ir.ui.menu'].get_user_roots()
        datas = request.env['ir.model.data'].sudo().search([
            ('model', '=', 'ir.ui.menu'),
            ('res_id', 'in', menu_roots.ids),
            ('module', 'in', module_names),
        ])

        shortcuts = []

        for module in module_ids:
            data = datas.filtered(lambda res: res.module == module.name)

            if data:
                shortcuts.append({
                    'name': module.display_name,
                    'url': '/web#menu_id=%s' % data.mapped('res_id')[0],
                    'description': module.summary,
                    'icons': [{
                        'sizes': '100x100',
                        'src': module.icon,
                        'type': mimetypes.guess_type(module.icon)[0] or 'image/png'
                    }]
                })

        return shortcuts

    @http.route('/web/manifest.webmanifest', type='http', auth='public', methods=['GET'])
    def webmanifest(self):
        """ Returns a WebManifest describing the metadata associated with a web application.
        Using this metadata, user agents can provide developers with means to create user
        experiences that are more comparable to that of a native application.
        """
        web_app_name = request.env['ir.config_parameter'].sudo().get_param('web.web_app_name', self._get_default_web_app_name())
        manifest = {
            'name': web_app_name,
            'scope': '/web',
            'start_url': '/web',
            'display': 'standalone',
            'background_color': self._get_manifest_background_color(),
            'theme_color': self._get_manifest_theme_color(),
            'prefer_related_applications': False,
        }
        icon_sizes = self._get_manifest_icon_sizes()
        manifest['icons'] = [{
            'src': icon_sizes.get(size),
            'sizes': size,
            'type': 'image/png',
        } for size in icon_sizes.keys()]
        manifest['shortcuts'] = self._get_shortcuts()
        body = json.dumps(manifest, default=ustr)
        response = request.make_response(body, [
            ('Content-Type', 'application/manifest+json'),
        ])

        return response

    def _icon_path(self):
        return self._get_offline_icon_path()

    @http.route('/web/offline', type='http', auth='public', methods=['GET'])
    def offline(self):
        """ Returns the offline page delivered by the service worker """
        return request.render('web.webclient_offline', {
            'app_name': request.env['ir.config_parameter'].sudo().get_param('web.web_app_name', self._get_default_web_app_name()),
            'app_icon': base64.b64encode(file_open(self._icon_path(), 'rb').read()),
            'app_icon_type': mimetypes.guess_type(self._icon_path())[0] or 'image/png',
            'bg_color': self._get_manifest_background_color(),
        })
