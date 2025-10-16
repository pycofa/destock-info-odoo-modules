# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import _, fields, models
from odoo.exceptions import UserError


class IapAccountUpdateBalanceWizard(models.TransientModel):
    _name = 'iap.account.update_balance.wizard'
    _description = 'Wizard to update balance of IAP Account with new balance'
    _transient_max_hours = 0.1

    account_id = fields.Many2one(
        'iap.account',
        string='IAP Account',
    )

    unit_name = fields.Char(
        string='Unit',
        readonly=True,
    )

    add_balance = fields.Float(
        'Add',
        required=True,
    )

    def action_update_balance(self):
        allowed_users = self.account_id._get_force_allowed_add_balance_users()

        if len(allowed_users) > 0 and self.env.user.login not in allowed_users:
            raise UserError(_('You are not allowed to update balance for this IAP account'))

        self.account_id.provider_balance += self.add_balance

        return {
            'type': 'ir.actions.act_window_close',
        }
