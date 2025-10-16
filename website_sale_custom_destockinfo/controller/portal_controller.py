# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo.addons.portal.controllers.portal import CustomerPortal, route, request


class CustomerPortalCustom(CustomerPortal):

    @route(['/my/account'], type='http', auth='user', website=True)
    def account(self, redirect=None, **post):
        request.update_context(infos_missing=request.params.get('infos_missing', '0') == '1')
        res = super().account(redirect, **post)
        return res
