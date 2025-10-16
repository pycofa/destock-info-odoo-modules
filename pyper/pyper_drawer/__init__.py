# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from . import models


def post_init_hook(env):
    icp = env['ir.config_parameter'].sudo()

    # Drawer
    if icp.get_param('pyper_drawer.drawer_props.showRootApp', None) is None:
        icp.set_param('pyper_drawer.drawer_props.showRootApp', 'True')

    if icp.get_param('pyper_drawer.drawer_props.alwaysFooter', None) is None:
        icp.set_param('pyper_drawer.drawer_props.alwaysFooter', 'True')

    if icp.get_param('pyper_drawer.drawer_props.hideCategoryLabelMinified', None) is None:
        icp.set_param('pyper_drawer.drawer_props.hideCategoryLabelMinified', 'True')

    if icp.get_param('pyper_drawer.drawer_props.hideNavbarAppsMenu', None) is None:
        icp.set_param('pyper_drawer.drawer_props.hideNavbarAppsMenu', 'True')

    if icp.get_param('pyper_drawer.drawer_props.fixedTop', None) is None:
        icp.set_param('pyper_drawer.drawer_props.fixedTop', 'True')

    if icp.get_param('pyper_drawer.drawer_props.minifiable', None) is None:
        icp.set_param('pyper_drawer.drawer_props.minifiable', 'True')

    if icp.get_param('pyper_drawer.drawer_props.popoverMinified', None) is None:
        icp.set_param('pyper_drawer.drawer_props.popoverMinified', 'True')

    if icp.get_param('pyper_drawer.drawer_props.closeOnClick', None) is None:
        icp.set_param('pyper_drawer.drawer_props.closeOnClick', 'True')

    if icp.get_param('pyper_drawer.drawer_props.closeAllUnactivatedItemsOnClick', None) is None:
        icp.set_param('pyper_drawer.drawer_props.closeAllUnactivatedItemsOnClick', 'True')

    if icp.get_param('pyper_drawer.drawer_props.subItemsDepth', None) is None:
        icp.set_param('pyper_drawer.drawer_props.subItemsDepth', '1')

    if icp.get_param('pyper_drawer.drawer_props.nextItemsSubPanel', None) is None:
        icp.set_param('pyper_drawer.drawer_props.nextItemsSubPanel', 'True')


def uninstall_hook(env):
    icp = env['ir.config_parameter'].sudo()
    icp.search([('key', 'like', 'pyper_drawer.%')]).unlink()
