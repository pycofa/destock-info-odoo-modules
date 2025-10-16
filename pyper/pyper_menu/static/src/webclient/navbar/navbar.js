/** @odoo-module **/

import {useState} from '@odoo/owl';
import {useService} from '@web/core/utils/hooks';
import {patch} from '@web/core/utils/patch';
import {NavBar} from '@web/webclient/navbar/navbar';

patch(NavBar.prototype, {
    setup() {
        super.setup();
        this.menuStateService = useState(useService('menu_state'));
    },

    get systemTrayItems() {
        const menu = this.menuService.getMenuAsTree('root');
        const items = [];

        (menu.childrenTree || []).forEach((menu) => {
            if ('system_tray' === menu.position) {
                items.push({
                    ...menu,
                    isActive: this.menuStateService.menuIsActivated(menu),
                });
            }
        });

        return items;
    },

    onNavBarDropdownItemSelection(menu) {
        super.onNavBarDropdownItemSelection(menu);

        // Force app changed to refresh the selection of menu
        if (menu) {
            this.env.bus.trigger('MENUS:APP-CHANGED');
        }
    },

    sectionIsSelected(menu) {
        if (this.currentApp && menu) {
            menu = typeof menu === 'number' ? this.menuService.getMenu(menu) : menu;

            // Check if selected menu is in sub menu or in children
            if (this.menuStateService.menuIsActivated(menu)) {
                return true;
            }

            // Check if selected menu is currentApp and if it is the case, check if the first sub menu is the same menu
            const currentApp = this.menuService.getCurrentApp();

            return currentApp.id === this.menuStateService.currentMenuId && currentApp?.childrenTree[0]?.id === menu.id;
        }

        return false;
    },
});
