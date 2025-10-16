# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import http
from odoo.http import request
from odoo.tools.safe_eval import safe_eval


class MenuItems(http.Controller):
    @http.route('/web/webclient/load_menu_counters', methods=['POST'], type='json', auth='user')
    def load_menu_counters(self, ids):
        menus = request.env['ir.ui.menu'].search([('id', 'in', ids)])
        values = {}

        for menu in menus:
            if menu.action:
                action = menu.action
                domain = []

                if 'domain' in action and action.domain:
                    domain = safe_eval(action.domain)

                values.update({menu.id: request.env[action.res_model].search_count(domain)})

        return {
            'menuCounters': values,
        }
