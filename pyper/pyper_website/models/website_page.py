# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import models


class WebsitePage(models.Model):
    _inherit = 'website.page'

    def write(self, vals):
        for page in self:
            # If URL has been edited directly in URL field of page, create permanently redirection
            if 'url' in vals:
                url = vals['url'] or ''

                if page.url != url and not isinstance(url, dict):
                    website_id = False

                    if vals.get('website_id') or page.website_id:
                        website_id = vals.get('website_id') or page.website_id.id

                    url = self.env['website'].with_context(website_id=website_id).get_unique_path(url)
                    page.menu_ids.write({'url': url})
                    self.env['website.rewrite'].create({
                        'name': vals.get('name') or page.name,
                        'redirect_type': '301',
                        'url_from': page.url,
                        'url_to': url,
                        'website_id': website_id,
                    })
                    vals['url'] = url

        return super(WebsitePage, self).write(vals)
