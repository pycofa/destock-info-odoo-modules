# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class IapAccount(models.Model):
    _inherit = 'iap.account'

    provider = fields.Selection(
        [
            ('odoo', 'Odoo IAP'),
        ],
        required=True,
        default='odoo',
    )

    provider_balance_enable = fields.Boolean(
        'Balance enable for provider?',
        compute='_compute_provider_balance_enable',
    )

    provider_balance_enabled = fields.Boolean(
        'Provider Balance enabled',
        default=False,
    )

    provider_balance = fields.Float(
        'Provider Balance',
        default=0.0,
        readonly=True,
    )

    provider_unit_name = fields.Char(
        'Provider Unit name',
        compute='_compute_provider_unit_name',
    )

    def get_services(self):
        if len(self.filtered(lambda a: not a.provider_balance_enable)) > 0:
            super().get_services()

    def _get_service_from_provider(self):
        """
        In case that the provider only propose one service you can return the service_name in you module to simplify
        the user interface.
        :return: str
        """
        return None

    def _check_provider_balance_enable(self):
        """
        Check if provider balance can be enabled for the selected provider.
        :return: bool
        """
        return False

    def _get_provider_unit_name(self):
        """
        Get the unit name of provider balance only if balance can be enabled.
        :return: str
        """
        return None

    def _get_force_allowed_add_balance_users(self):
        """
        Force to allow only the user logins defined in this list.
        :return: list[str]
        """
        return []

    def _set_service_from_provider(self):
        for account in self:
            service = account._get_service_from_provider()

            if service and account.service_name != service:
                account.service_name = service

    @api.model_create_multi
    def create(self, vals_list):
        accounts = super().create(vals_list)
        accounts._set_service_from_provider()

        return accounts

    def write(self, vals):
        if 'provider_balance_enabled' in vals:
            for account in self:
                allowed_users = account._get_force_allowed_add_balance_users()

                if len(allowed_users) > 0 and self.env.user.login not in allowed_users:
                    raise UserError(_('You are not allowed to enable or disable balance for this IAP Account'))

        super().write(vals)
        self._set_service_from_provider()

        for account in self:
            if account.provider_balance < 0.0:
                account.provider_balance = 0.0

        return True

    @api.depends('provider')
    def _compute_provider_balance_enable(self):
        for account in self:
            account.provider_balance_enable = account._check_provider_balance_enable()

    @api.depends('provider')
    def _compute_provider_unit_name(self):
        for account in self:
            account.provider_unit_name = account._get_provider_unit_name()

    @api.depends('account_info_id', 'provider', 'provider_balance_enabled')
    def _compute_balance(self):
        super()._compute_balance()

        for account in self:
            if account.provider_balance_enable:
                enabled = account.provider_balance_enabled
                account.balance = f'{account.provider_balance} {account.provider_unit_name}' if enabled else ''

    @api.onchange('provider', 'provider_balance_enabled')
    def _onchange_provider_info(self):
        for account in self:
            if not account.provider_balance_enable:
                account.provider_balance_enabled = False

            if not account.provider_balance_enabled:
                account.provider_balance = 0.0

            account._reset_account_provider_info()

    def _reset_account_provider_info(self):
        self.ensure_one()

    def action_update_balance(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Update balance'),
            'res_model': 'iap.account.update_balance.wizard',
            'view_mode': 'form',
            'target': 'new',
            'view_id': self.env.ref('pyper_iap.view_iap_account_update_balance_wizard', False).id,
            'context': {**self.env.context, **{
                'default_account_id': self.id,
                'default_unit_name': self.provider_unit_name,
            }},
        }
