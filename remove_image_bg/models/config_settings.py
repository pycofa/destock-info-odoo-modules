# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    rembg_api_key = fields.Char('API KEY remove.bg', config_parameter='remove_image_bg.rembg_api_key')
