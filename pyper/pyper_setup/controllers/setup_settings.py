# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo.http import Controller, route, request
from odoo.osv.expression import OR


class SetupSettings(Controller):
    @route('/pyper_setup/settings', type='json', auth='user')
    def setup_settings(self, prefix=None):
        if not prefix:
            return []

        prefixes = prefix.split('|')
        domains = []

        for prefix in prefixes:
            domains.append([('key', 'like', str(prefix) + '%')])

        return request.env['ir.config_parameter'].sudo().search_read(
            OR(domains),
            ['key', 'value'],
        )
