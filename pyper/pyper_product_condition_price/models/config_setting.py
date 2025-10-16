# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models, _
import requests
import base64
from odoo.exceptions import UserError
import time


class ConfSetting(models.TransientModel):
    _inherit = "res.config.settings"

    group_product_show_custom_sale_price = fields.Boolean(
        "Show variant sale price",
        implied_group='pyper_product_condition_price.group_product_show_custom_sale_price'
    )

