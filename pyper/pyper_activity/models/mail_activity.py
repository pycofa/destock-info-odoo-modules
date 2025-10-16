# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import models


class MailActivity(models.Model):
    _inherit = 'mail.activity'

    def _action_done(self, feedback=False, attachment_ids=None):
        """
        Replace native active_done method to avoid deleting of activities done.
        """
        return self._override_action_done(feedback, attachment_ids)

    def _override_action_done(self, feedback=False, attachment_ids=None):
        """
        Replace native active_done method to avoid deleting of activities done.
        """
        self.active = False

        messages = self.env['mail.message']
        next_activities = self.env['mail.activity']

        return messages, next_activities
