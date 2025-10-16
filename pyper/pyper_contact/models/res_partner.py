# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models, api, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_user = fields.Boolean(
        'Is user',
        compute="_compute_is_user",
        store=True,
    )

    @api.depends('user_ids')
    def _compute_is_user(self):
        for partner in self:
            partner.is_user = len(partner.user_ids) > 0

