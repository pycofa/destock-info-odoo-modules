/** @odoo-module **/

import {Component} from '@odoo/owl';

export class MenuBreadcrumbItem extends Component {
    static template = 'pyper_menu.MenuBreadcrumbItem';

    static props = {
        label: {
            type: String,
        },
        active: {
            type: Boolean,
            optional: true,
        },
    };

    static defaultProps = {
        active: false,
    };
}
