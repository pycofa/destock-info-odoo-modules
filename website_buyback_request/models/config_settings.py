# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    email_to = fields.Char('Email To', config_parameter='website_buyback_request.email_to')
    email_cc = fields.Char('Email CC', config_parameter='website_buyback_request.email_cc')
