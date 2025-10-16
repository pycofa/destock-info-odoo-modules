# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).
from email.policy import default

from odoo import api, fields, models


class ConfSetting(models.TransientModel):
    _inherit = "res.config.settings"


    ecommerce_show_form_quotation = fields.Boolean(
        "Display form for quotation in ecommerce",
        config_parameter='website_sale_quotation.ecommerce_show_form_quotation'
    )

    email_to_for_quotation = fields.Char(config_parameter='website_sale_quotation.email_to_for_quotation')
    email_cc_for_quotation = fields.Char(config_parameter='website_sale_quotation.email_cc_for_quotation')

    allow_quotation_settings = fields.Boolean(
        compute='_compute_allow_quotation_settings',
        store=True,
    )

    @api.depends('ecommerce_show_add_to_cart')
    def _compute_allow_quotation_settings(self):
        if not self.ecommerce_show_add_to_cart:
            self.allow_quotation_settings = True
        else:
            self.allow_quotation_settings = False
            if self.ecommerce_show_form_quotation:
                self.ecommerce_show_form_quotation = False
