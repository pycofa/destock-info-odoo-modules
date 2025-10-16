# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from . import models

def post_init_hook(env):
    env['res.config.settings'].create({
        'group_product_variant': True,  # Activate variant
    }).execute()
