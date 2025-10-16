/** @odoo-module **/

import {Component, onMounted, useState} from '@odoo/owl';
import {useService} from '@web/core/utils/hooks';
import {MenuBreadcrumbItem} from './menu_breadcrumb_item';

export class MenuBreadcrumb extends Component {
    static template = 'pyper_menu.MenuBreadcrumb';

    static components = {
        MenuBreadcrumbItem,
    };

    static props = {};

    setup() {
        this.menuService = useState(useService('menu'));
        this.menuStateService = useState(useService('menu_state'));
        this.state = useState({
            mounted: false,
        })

        onMounted(() => {
            this.state.mounted = true;
        })
    }

    get mounted() {
        return this.state.mounted;
    }

    get activeMenus() {
        return this.menuStateService.activeIds.map(menuId => this.menuService.getMenu(menuId));
    }

    get activeBreadcrumbMenus() {
        return this.activeMenus.slice(1);
    }

    isActiveMenu(menuId) {
        return this.menuStateService.currentMenuId === menuId;
    }
}
