# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import http
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.http import request


class WebsiteSaleDisabled(WebsiteSale):

	@http.route(['/shop/cart'], type='http', auth="public", website=True, sitemap=False)
	def cart(self, access_token=None, revive='', **post):
		able_to_cart = request.env['ir.config_parameter'].sudo().get_param('website_sale_disable_cart.ecommerce_show_add_to_cart')

		if not able_to_cart:
			return request.redirect('/shop')
		else:
			return super().cart(access_token, revive, **post)
