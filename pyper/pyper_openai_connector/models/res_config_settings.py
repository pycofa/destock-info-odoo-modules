# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    openai_token_api = fields.Char(
        string="Open AI Token API",
        store=True,
        config_parameter='pyper_openai_connector.openai_token_api',
    )
