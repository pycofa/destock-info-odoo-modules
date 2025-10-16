# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import http
from odoo.http import request
from odoo.addons.mail.controllers.thread import ThreadController as BaseThreadController


class ThreadController(BaseThreadController):
    @http.route('/mail/thread/messages', methods=['POST'], type='json', auth='user')
    def mail_thread_messages(self, thread_model, thread_id, search_term=None, before=None, after=None, around=None, limit=30):
        if self._include_children_messages(thread_model):
            request.update_context(mail_message_with_children_res_ids=request.env[thread_model].search([('parent_id', '=', thread_id)]).ids)

        return super().mail_thread_messages(thread_model, thread_id, search_term, before, after, around, limit)

    def _include_children_messages(self, thread_model):
        return thread_model == 'res.partner'
