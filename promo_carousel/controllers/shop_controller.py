# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).
from itertools import product

from odoo import http
from odoo.addons.website_sale.controllers.main import WebsiteSale, TableCompute
from odoo.http import request
import re


class WebsiteSaleCustom(WebsiteSale):

	@http.route([
		'/shop',
		'/shop/page/<int:page>',
		'/shop/category/<model("product.public.category"):category>',
		'/shop/category/<model("product.public.category"):category>/page/<int:page>',
	], type='http', auth="public", website=True)
	def shop(self, page=0, category=None, search='', min_price=0.0, max_price=0.0, ppg=False, **post):
		res = super().shop(page=page, category=category, search=search, min_price=min_price, max_price=max_price, ppg=ppg, **post)

		promo_ids = request.env['promo.carousel'].search([])
		if promo_ids:
			res.qcontext.update({
                'promos': promo_ids
            })
        
		return res