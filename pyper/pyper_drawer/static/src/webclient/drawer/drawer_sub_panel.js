/** @odoo-module **/

import {Component, useState} from '@odoo/owl';
import {useService} from '@web/core/utils/hooks';
import {DrawerMenuItem} from './drawer_menu_item';
import {stylesToString} from '@pyper/core/ui/css';

export class DrawerSubPanel extends Component {
    static template = 'pyper_drawer.DrawerSubPanel';

    static components = {
        DrawerMenuItem: DrawerMenuItem,
    };

    static props = {};

    setup() {
        this.drawerService = useState(useService('drawer'));
    }

    get classes() {
        return {
            'o_drawer--sub-panel': true,
            'o_drawer': true, // Use to retrieve the same style of drawer component
            'o_drawer--ready': this.isMounted,
            'o_drawer--opened': this.isDrawerOpened,
            'o_drawer--locked': this.isDrawerLocked,
            'o_drawer--drawer-mini': this.isDrawerMinified,
            'o_drawer--drawer-dragging': this.isDrawerDragging,
            'o_drawer--sub-panel--opened': this.isOpened,
            'o_drawer--nav': this.isNav,
            'o_drawer--fixed-top': this.isFixedTop,
        };
    }

    get styles() {
        return stylesToString({
            '--drawer-margin-fixed-top': this.drawerService.neutralizeBannerTop + 'px',
        });
    }

    get isMounted() {
        return this.drawerService.mounted;
    }

    get isDrawerOpened() {
        return this.drawerService.isOpened;
    }

    get isDrawerLocked() {
        return this.drawerService.isLocked;
    }

    get isDrawerMinified() {
        return this.drawerService.isMinified;
    }

    get isDrawerDragging() {
        return this.drawerService.dragging;
    }

    get isOpened() {
        return this.drawerService.isSubPanelOpened;
    }

    get isNav() {
        return this.drawerService.isNav;
    }

    get isFixedTop() {
        return this.drawerService.isFixedTop;
    }

    get title() {
        return this.drawerService.subPanelMenu?.name;
    }

    get menu() {
        return this.drawerService.subPanelMenu;
    }

    get menuChildren() {
        return this.drawerService.subPanelMenu?.childrenTree || [];
    }
}
