# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import models


class MailActivity(models.Model):
    _inherit = 'mail.activity'

    def _action_done(self, feedback=False, attachment_ids=None):
        vals_activities = []

        for model, activity_data in self._classify_by_model().items():
            for activity in activity_data['activities']:
                vals_activities.append({
                    'id': activity.id,
                    'subject': activity.summary,
                    'author_id': activity.user_id.partner_id,
                    'body': activity.note,
                })

        res = super()._action_done(feedback=feedback, attachment_ids=attachment_ids)

        for message, activity in zip(res[0], vals_activities):
            message.subject = activity.get('subject', False)
            message.author_id = activity.get('author_id', False)
            message.body = activity.get('body', False)
            message.feedback = feedback

            if message.mail_activity_type_id and message.mail_activity_type_id.id == self.env.ref('mail.mail_activity_data_email').id:
                message.message_type = 'email_outgoing'

        return res
