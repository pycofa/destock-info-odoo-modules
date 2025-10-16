/** @odoo-module **/

import {reactive} from '@odoo/owl';
import {registry} from '@web/core/registry';


export class MenuState {
    constructor(bus, menu) {
        /** @type {import("@bus/services/bus_service").busService} */
        this.bus = bus;
        /** @type {import("@web/webclient/menus/menu_service").menuService} */
        this.menuService = menu;
    }

    setup() {
        this.state = {
            currentMenuId: undefined,
        };
    }

    get currentMenuId() {
        return this.state.currentMenuId;
    }

    set currentMenuId(menuId) {
        this.state.currentMenuId = menuId;
        this.bus.trigger('MENU-STATE:MENU-SELECTED', menuId);
    }

    get activeIds() {
        return this.currentMenuId ? Array.from(new Set([...this.findParentIds(this.currentMenuId), this.currentMenuId])) : [];
    }

    menuIsActivated(menu) {
        menu = typeof menu === 'number' ? this.menuService.getMenu(menu) : menu;

        if (typeof menu === 'object') {
            if (this.activeIds.includes(menu.id)) {
                return true;
            }

            try {
                const currentMenu = this.menuService.getMenuAsTree(this.currentMenuId);

                if (currentMenu && currentMenu.children && currentMenu.children[0] === menu.id) {
                    return true;
                }
            } catch (e) {
                // Allowed to skip error to return false value
            }
        }

        return  false;
    }

    findParentIds(targetMenuId) {
        if (!targetMenuId) {
            return [];
        }

        for (const menu of this.menuService.getAll()) {
            if (menu.id === targetMenuId) {
                return [...(menu['parentPath'] || [])];
            }
        }

        return [];
    }

    findAllChildrenIds(targetMenuId) {
        const menu = targetMenuId ? this.menuService.getMenuAsTree(targetMenuId) : undefined;

        if (!menu) {
            return [];
        }

        const ids = [menu.id];

        function getChildrenIds(childMenu) {
            ids.push(childMenu.id);
            (childMenu.childrenTree || []).forEach(getChildrenIds);
        }

        menu.childrenTree.forEach(getChildrenIds);

        return ids;
    }
}

export const menuStateService = {
    dependencies: ['menu'],
    start(env, {menu}) {
        const menuState = reactive(new MenuState(env.bus, menu));
        menuState.setup();

        return menuState;
    },
};

registry.category('services').add('menu_state', menuStateService);
