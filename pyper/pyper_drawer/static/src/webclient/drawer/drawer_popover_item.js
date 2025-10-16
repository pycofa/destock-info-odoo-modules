/** @odoo-module **/

import {Component, useState} from '@odoo/owl';
import {useService} from '@web/core/utils/hooks';

export class DrawerPopoverItem extends Component {
    static template = 'pyper_drawer.DrawerPopoverItem';

    static props = {
        '*': {optional: true},
    };

    setup() {
        this.menuStateService = useState(useService('menu_state'));
    }

    get classes() {
        return {
            'dropdown-item': true,
            'o_drawer--menu-item': true,
            'o_drawer--menu-item-active': this.isActive,
            'd-flex': true,
            'align-items-center': true,
        };
    }

    get isActive() {
        if (undefined === this.props.active) {
            return this.menuStateService.menuIsActivated(this.props.menuId);
        }

        return this.props.active;
    }
}
