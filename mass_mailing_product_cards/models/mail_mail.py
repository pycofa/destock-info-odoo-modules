# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import api, models


class MassMailing(models.Model):
    _inherit = 'mailing.mailing'
    
    
    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        if res.mail_server_id:
            res.email_from = res.mail_server_id.smtp_user
        if self.env.company.email:
            res.reply_to = self.env.company.email
        return res
