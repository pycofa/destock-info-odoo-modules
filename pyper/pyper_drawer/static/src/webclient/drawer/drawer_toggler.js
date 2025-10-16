/** @odoo-module **/

import {Component, onWillStart, onWillUpdateProps, onWillDestroy, useState} from '@odoo/owl';
import {useService} from '@web/core/utils/hooks';


export class DrawerToggler extends Component {
    static template = 'pyper_drawer.DrawerToggler';

    static props = {
        autoHide: {
            type: Boolean,
            optional: true,
        },
        useCaretIcon: {
            type: Boolean,
            optional: true,
        },
    };

    static defaultProps = {
        autoHide: undefined,
        useCaretIcon: undefined,
    };

    static configurableDefaultProps = {
        autoHide: false,
        useCaretIcon: false,
    };

    static SETUP_PREFIX = 'pyper_drawer.drawer_toggler_props.';

    setup() {
        this.pyperSetupService = useService('pyper_setup');
        this.drawerService = useState(useService('drawer'));

        onWillStart(async () => {
            await this.pyperSetupService.register(DrawerToggler.SETUP_PREFIX, DrawerToggler.configurableDefaultProps);
        });

        onWillDestroy(() => {
            this.pyperSetupService.unregister(DrawerToggler.SETUP_PREFIX);
        });

        onWillUpdateProps((nextProps) => {
            this.pyperSetupService.onWillUpdateProps(DrawerToggler.SETUP_PREFIX, nextProps);
        });
    }

    get settings() {
        return this.pyperSetupService.settings[DrawerToggler.SETUP_PREFIX] || {};
    }

    get classes() {
        return {
            'o-dropdown': true,
            'dropdown': true,
            'o_drawer_toggler': true,
            'o-dropdown--no-caret': true,
            'o_drawer--locked': this.drawerService.isLocked,
            'o_drawer--mini': this.drawerService.isMinified,
            'o_drawer--fixed-top': this.drawerService.isFixedTop,
        };
    }

    get displayMenuIcon() {
        return !this.settings.useCaretIcon || (this.settings.useCaretIcon && !this.drawerService.isMinified);
    }

    get displayCaretIcon() {
        return this.settings.useCaretIcon && this.drawerService.isMinified;
    }

    get display() {
        if (this.settings.autoHide) {
            if (this.drawerService.isSmallScreen) {
                return !this.drawerService.disabledOnSmallScreen;
            } else {
                if (this.drawerService.disabledOnSmallScreen) {
                    return true;
                } else {
                    return !this.drawerService.isLocked;
                }
            }
        }

        return !(this.drawerService.isSmallScreen && this.drawerService.disabledOnSmallScreen);
    }

    onClick() {
        this.drawerService.toggle();
    }
}
