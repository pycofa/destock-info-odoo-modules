# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models, _


class BlogPost(models.Model):
    _inherit = 'blog.blog'

    ai_description = fields.Text(
        'AI Description',
        help=_('This field will help AI to understand general prompt about what is needed for result.')
    )
