# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).
from email.policy import default

from odoo import api, fields, models


class ConfSetting(models.TransientModel):
    _inherit = "res.config.settings"

    ecommerce_show_add_to_cart = fields.Boolean(
        string='Allow add to cart in ecommerce',
        config_parameter='website_sale_disable_cart.ecommerce_show_add_to_cart',
    )
