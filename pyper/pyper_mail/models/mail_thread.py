# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import _, models


class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    def _creation_message(self):
        if self._name == 'res.partner':
            self.ensure_one()

            if self.company_type == 'person':
                return _('The contact %s was created', self[self._rec_name])

            return _('The company %s was created', self[self._rec_name])

        return super()._creation_message()
