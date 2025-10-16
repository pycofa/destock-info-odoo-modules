/** @odoo-module */

import {registry} from '@web/core/registry';
import '@web/webclient/menus/menu_providers'

const commandProviderRegistry = registry.category('command_provider');
const menu = commandProviderRegistry.get('menu');
const menuProvideFct = menu.provide;

const MENU_SETUP_PREFIX = 'pyper_menu.provider.';

menu.provide = async function (env, options) {
    const menuService = env.services.menu;
    const pyperSetupService = env.services['pyper_setup'];
    const res = await menuProvideFct(env, options);

    await pyperSetupService.register(MENU_SETUP_PREFIX, {
        preferWebIcon: false,
    });

    res.forEach((item) => {
        const usp = new URLSearchParams(item.href.replace('#', ''));
        const menuId = usp.get('menu_id');

        if (menuId) {
            const menu = menuService.getMenu(menuId);

            if (item?.props?.webIconData?.includes('/web_enterprise/static/img/default_icon_app.png')) {
                delete item.props.webIconData;
            }

            if ((menu.fontIcon || menu.fontIconColor) && item.props) {
                item.props.webIcon = {
                    iconClass: menu.fontIcon,
                    color: menu.fontIconColor,
                    backgroundColor: undefined,
                };

                if (!pyperSetupService.settings[MENU_SETUP_PREFIX].preferWebIcon) {
                    delete item.props.webIconData;
                }
            }
        }
    });

    return res;
};
