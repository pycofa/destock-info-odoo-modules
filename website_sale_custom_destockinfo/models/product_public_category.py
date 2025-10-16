# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class ProductPublicCategory(models.Model):
    _inherit = 'product.public.category'

    icon_image_1920 = fields.Image("Icon", max_width=1920, max_height=1920)
    icon_image_1024 = fields.Image("Icon 1024", related="image_1920", max_width=1024, max_height=1024, store=True)
    icon_image_512 = fields.Image("Icon 512", related="image_1920", max_width=512, max_height=512, store=True)
    icon_image_256 = fields.Image("Icon 256", related="image_1920", max_width=256, max_height=256, store=True)
    icon_image_128 = fields.Image("Icon 128", related="image_1920", max_width=128, max_height=128, store=True)
