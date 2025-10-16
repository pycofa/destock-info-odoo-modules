# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import api, fields, models


class MailMessage(models.Model):
    _inherit = 'mail.message'

    feedback = fields.Text(
        'Feedback',
    )

    mail_activity_type_icon = fields.Char(
        related='mail_activity_type_id.icon',
    )

    mail_activity_type_name = fields.Char(
        related='mail_activity_type_id.name',
    )

    def _message_format_extras(self, format_reply):
        self.ensure_one()
        vals = super()._message_format_extras(format_reply)
        vals.update({
            'feedback': self.feedback or False,
            'mail_activity_type_icon': self.mail_activity_type_icon,
            'mail_activity_type_name': self.mail_activity_type_name,
        })

        return vals

    @api.model
    def _message_fetch(self, domain, search_term=None, before=None, after=None, around=None, limit=30):
        res_ids = self.env.context.get('mail_message_with_children_res_ids', False)

        if res_ids:
            domain[:0] = [
                '|',
                ('res_id', 'in', res_ids),
            ]

        return super()._message_fetch(domain, search_term, before, after, around, limit)
