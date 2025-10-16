# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import api, fields, models


class IapAccount(models.Model):
    _inherit = 'iap.account'

    provider_warn_me = fields.Boolean(
        'Provider Warn me',
        default=False,
    )

    provider_warning_threshold = fields.Float(
        'Provider Threshold',
        default=0.0,
    )

    provider_warning_email = fields.Char(
        'Provider Warning email',
    )

    provider_warning_template_id = fields.Many2one(
        'mail.template',
        'Provider Warning template',
        domain=[('model', '=', 'iap.account')],
    )

    warning_threshold = fields.Float(
        'Threshold',
        compute='_compute_warning_threshold',
        inverse='_inverse_warning_threshold',
        related=None,
    )

    @api.depends('account_info_id', 'account_info_id.warning_threshold', 'provider_warning_threshold')
    def _compute_warning_threshold(self):
        for account in self:
            if account.account_info_id:
                account.warning_threshold = account.account_info_id.warning_threshold
            else:
                account.warning_threshold = account.provider_warning_threshold

    def _inverse_warning_threshold(self):
        for account in self:
            if account.account_info_id:
                account.account_info_id.warning_threshold = account.warning_threshold

    def _reset_account_provider_info(self):
        super()._reset_account_provider_info()

        if not self.provider_balance_enabled:
            self.provider_warn_me = False

        if not self.provider_warn_me:
            self.provider_warning_threshold = 0.0
            self.provider_warning_email = False

    def write(self, values):
        res = super(IapAccount, self).write(values)

        for account in self:
            if (account.provider_balance_enabled
                    and account.provider_warn_me
                    and account.provider_warning_email
                    and account.provider_warning_template_id
                    and values.get('provider_balance', 0.0) < account.provider_warning_threshold):
                account.provider_warning_template_id.send_mail(account.id, email_values={
                    'email_to': account.provider_warning_email,
                })

        return res
