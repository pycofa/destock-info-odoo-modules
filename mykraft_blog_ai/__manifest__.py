# Copyright Krafter SAS <hey@krafter.io>
# Odoo Proprietary License (see LICENSE file).

{
    'name': 'myKraft blog AI',
    'category': 'Hidden/Tools',
    'license': 'Other proprietary',
    'description': 'This addon will allow to write blog posts with OpenAI Connector',
    'summary': 'This addon will allow to write blog posts with OpenAI Connector',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'installable': True,
    'depends': [
        'mykraft_blog',
        'website_blog',
    ],
    'data': [
        # Views
        'views/website_blog_views.xml',
        'views/blog_post_add.xml',
    ],
}
