/** @odoo-module **/

import {Component, useState} from '@odoo/owl';
import {useService} from '@web/core/utils/hooks';


export class DrawerAppMenu extends Component {
    static template = 'pyper_drawer.DrawerAppMenu';

    static props = {
        minified: {
            type: Boolean,
            optional: true,
        },
        slots: {
            type: Object,
            optional: true,
        },
    }

    static defaultProps = {
        minified: false,
    }

    setup() {
        this.drawerService = useState(useService('drawer'));
    }

    get displayMinified() {
        return this.drawerService.isMinified || this.drawerService.disabledOnSmallScreen || this.props.minified;
    }

    get displayLocked() {
        return !this.displayMinified && (this.drawerService.isLocked || (this.drawerService.locked && !this.drawerService.isLocked && this.drawerService.isOpened));
    }
}
