# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).
from email.policy import default

from odoo import api, fields, models


class ConfSetting(models.TransientModel):
    _inherit = "res.config.settings"

    group_ecommerce_show_qty_available = fields.Boolean(
        string='Allow to show available quantity in shop ecommerce',
        implied_group='website_sale_only_available_attributes.group_ecommerce_show_qty_available',
    )

    @api.model
    def get_values(self):
        res = super().get_values()
        res.update(
            group_ecommerce_show_qty_available=self.env['ir.config_parameter']
			.sudo().get_param('website_sale_only_available_attributes.group_ecommerce_show_qty_available', default=False)
        )
        return res

    @api.model
    def set_values(self):
        super().set_values()
        self.env['ir.config_parameter'].sudo().set_param('website_sale_only_available_attributes.group_ecommerce_show_qty_available',
														 self.group_ecommerce_show_qty_available)
