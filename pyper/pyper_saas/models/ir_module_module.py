# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo.addons.base.models.ir_module import Module

_origin_get_values_from_terp = Module.get_values_from_terp


def get_values_from_terp(self, terp=None):
    """
    Override static method 'get_values_from_terp' to hide uninstallable addons.
    """
    if terp is None:
        terp = self

    res = _origin_get_values_from_terp(terp)

    if terp.get('to_buy', False) and not res.get('to_buy', False):
        res.update({'to_buy': True})

    return res


Module.get_values_from_terp = get_values_from_terp
