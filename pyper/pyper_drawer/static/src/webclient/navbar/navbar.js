/** @odoo-module **/

import {patch} from '@web/core/utils/patch';
import {useService} from '@web/core/utils/hooks';
import {NavBar} from '@web/webclient/navbar/navbar';
import {Drawer} from '../drawer/drawer';
import {DrawerAppMenu} from '../drawer/drawer_app_menu';
import {DrawerMenuItem} from '../drawer/drawer_menu_item';
import {DrawerToggler} from '../drawer/drawer_toggler';

patch(NavBar.prototype, {
    setup() {
        super.setup();

        this.drawerService = useService('drawer');
    },

    get drawerNextItemsSubPanel() {
        return this.drawerService.nextItemsSubPanel;
    },

    get currentAppSections() {
        if (this.drawerNextItemsSubPanel) {
            return [];
        }

        return super.currentAppSections;
    },
});

NavBar.components.Drawer = Drawer;
NavBar.components.DrawerAppMenu = DrawerAppMenu;
NavBar.components.DrawerMenuItem = DrawerMenuItem;
NavBar.components.DrawerToggler = DrawerToggler;
