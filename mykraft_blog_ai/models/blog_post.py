# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from openai import OpenAI


class BlogPost(models.Model):
    _inherit = 'blog.post'

    write_with_ai = fields.Boolean(
        'Write with AI ?',
    )

    ai_prompt = fields.Text(
        'AI prompt',
        help=_('Add information for AI here, prompt is not mandatory.')
    )

    def create(self, vals):
        res = super().create(vals)

        if 'write_with_ai' in vals and 'name' in vals and 'blog_id' in vals:
            prompt = 'J\'aimerais que tu rédige un article de blog avec pour titre :' + vals.get('name') + '.'

            blog = self.env['blog.blog'].browse(vals['blog_id'])

            if blog.ai_description:
                prompt += ' Je te donne des éléments qui sont inscrits comme des standards dans le cadre de mon blog. Les voici : ' + blog.ai_description

            openai_token = self.env['ir.config_parameter'].sudo().get_param('pyper_openai_connector.openai_token_api')

            if not openai_token:
                raise UserError(_('You have to fill Open AI Token first in order to enrich flow data.'))

            client = OpenAI(
                api_key=openai_token
            )

            response = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="gpt-4o",
            )

            response_html = response.choices[0].message.content
            response_html = response_html.replace("```html", "").replace("```", "").strip()

            res.content = response_html

        return res
