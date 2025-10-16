# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class ConfSetting(models.TransientModel):
    _inherit = 'res.config.settings'

    group_product_show_variant_standard_price = fields.Boolean(
        'Show variant standard price',
        implied_group='pyper_product_condition.group_product_show_variant_standard_price',
    )

    group_product_show_variant_list_price = fields.Boolean(
        'Show variant list price',
        implied_group='pyper_product_condition.group_product_show_variant_list_price',
    )
