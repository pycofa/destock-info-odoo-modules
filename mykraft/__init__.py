# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from . import controllers
from . import models


def post_init_hook(env):
    icp = env['ir.config_parameter'].sudo()

    # Drawer
    if icp.get_param('pyper_drawer.drawer_props.nav', None) is None:
        icp.set_param('pyper_drawer.drawer_props.nav', 'True')

    if icp.get_param('pyper_drawer.drawer_props.fixedTop', None) == 'True':
        icp.set_param('pyper_drawer.drawer_props.fixedTop', False)

    if icp.get_param('pyper_drawer.drawer_props.alwaysHeader', None) is None:
        icp.set_param('pyper_drawer.drawer_props.alwaysHeader', 'True')

    if icp.get_param('pyper_drawer.drawer_props.minifiable', None) == 'True':
        icp.set_param('pyper_drawer.drawer_props.minifiable', False)

    if icp.get_param('pyper_drawer.drawer_props.hideCategoryLabelFull', None) == 'True':
        icp.set_param('pyper_drawer.drawer_props.hideCategoryLabelFull', False)

    if icp.get_param('pyper_drawer.drawer_props.subItemsDepth', None) is None:
        icp.set_param('pyper_drawer.drawer_props.subItemsDepth', '1')
