/** @odoo-module **/

import {Component, onWillUpdateProps, useEffect, useRef, useState} from '@odoo/owl';
import {DropdownItem} from '@web/core/dropdown/dropdown_item';
import {usePopover} from '@web/core/popover/popover_hook';
import {useBus, useService} from '@web/core/utils/hooks';
import {humanNumber} from '@web/core/utils/numbers';
import {findFirstSelectableMenu} from '@pyper/webclient/menus/menu_helpers';
import {DrawerPopoverItem} from './drawer_popover_item';


export class DrawerMenuItem extends Component {
    static template = 'pyper_drawer.DrawerMenuItem';

    static components = {
        DropdownItem: DropdownItem,
        DrawerMenuItem: DrawerMenuItem,
    };

    static props = {
        menuXmlid: {
            type: String,
            optional: true,
        },
        menuId: {
            type: [Number, String],
            optional: true,
        },
        menuAction: {
            type: [String, Number],
            optional: true,
        },
        hotkey: {
            type: String,
            optional: true,
        },
        childrenDepth: {
            type: Number,
            optional: true,
        },
        children: {
            type: Array,
            optional: true,
        },
        withIcon: {
            type: Boolean,
            optional: true,
        },
        iconData: {
            optional: true,
        },
        fontIcon: {
            type: String,
            optional: true,
        },
        fontIconColor: {
            type: String,
            optional: true,
        },
        emojiIcon: {
            type: String,
            optional: true,
        },
        label: {
            type: String,
            optional: true,
        },
        active: {
            type: Boolean,
            optional: true,
        },
        depth: {
            type: Number,
            optional: true,
        },
        disablePopover: {
            type: Boolean,
            optional: true,
        },
        preferWebIcon: {
            type: Boolean,
            optional: true,
        },
        className: {
            type: String,
            optional: true,
        },
        onSelection: {
            type: Function,
            optional: true,
        },
    }

    static defaultProps = {
        childrenDepth: 0,
        children: [],
        withIcon: false,
        active: undefined,
        depth: 0,
        disablePopover: false,
        preferWebIcon: false,
    }

    setup() {
        this.drawerService = useState(useService('drawer'));
        this.menuStateService = useState(useService('menu_state'));
        this.menuCounterService = useState(useService('menu_counter'));
        this.actionService = useService('action');
        this.menuService = useService('menu');
        this.content = useRef('content');
        this.state = useState({
            opened: this.menuStateService.menuIsActivated(this.props.menuId),
        });

        if (!this.drawerService.popover) {
            const navCls = (this.drawerService.isNav ? ' o_drawer--popover-item-nav' : '');
            this.drawerService.popover = usePopover(DrawerPopoverItem, {
                position: 'right-middle',
                animation: false,
                arrow: false,
                fixedPosition: false,
                popoverClass: 'o_drawer--popover-item' + navCls,
            });
        }

        onWillUpdateProps((nextProps) => this.onWillUpdateProps(nextProps));

        useBus(this.env.bus, 'MENU-STATE:MENU-SELECTED', this.onMenuItemSelected.bind(this));
        useBus(this.env.bus, 'DRAWER:OPEN-MENU', this.onMenuItemOpened.bind(this));

        useEffect((menuId) => {
            this.menuCounterService.unregisterMenuItem(this.props.menuId);

            const menu = this.menuService.getMenu(this.props.menuId);

            if (menu?.displayCounter) {
                this.menuCounterService.registerMenuItem(menuId);
            }
        }, () => [this.props.menuId]);
    }

    get classes() {
        return {
            'o_drawer--menu-item': true,
            'o_drawer--menu-item-with-icon': this.displayIcon,
            'o_drawer--menu-item-active': this.isActive,
            'o_drawer--menu-item-opened': this.isOpened,
            ...(this.props.className || '').split(' ').reduce((obj, cls) => ({...obj, [cls]: true}), {}),
        };
    }

    get styles() {
        return {
            '--drawer-item-depth': this.props.depth,
        };
    }

    get hasChildren() {
        return this.props.childrenDepth !== 0 && this.children.length > 0;
    }

    get displayChildren() {
        return !this.isPopoverEnabled && this.hasChildren && this.children.length > 1;
    }

    get displayIcon() {
        return this.props.withIcon || !!this.props.fontIcon || !!this.props.emojiIcon;
    }

    get isPopoverEnabled() {
        return !this.props.disablePopover && this.drawerService.isMinified && this.drawerService.popoverMinified;
    }

    get isNextChildrenEnabled() {
        return this.drawerService.nextItemsSubPanel && this.children?.length > 1 && this.props.childrenDepth === 0;
    }

    get isNextChildrenOpened() {
        return this.isNextChildrenEnabled && this.drawerService.subPanelMenu?.id === this.menu?.id;
    }

    get menuItemHref() {
        if (!this.props.menuId && !this.props.menuAction && !this.props.onSelection) {
            return undefined;
        }

        const parts = [];

        if (this.props.menuId) {
            parts.push(`menu_id=${this.props.menuId}`);
        }

        if (this.props.menuAction) {
            parts.push(`action=${this.props.menuAction}`);
        }

        return '#' + parts.join('&');
    }

    get isActive() {
        if (undefined === this.props.active) {
            return this.menuStateService.menuIsActivated(this.props.menuId);
        }

        return this.props.active;
    }

    get isOpened() {
        return this.state.opened;
    }

    get children() {
        return this.props.children;
    }

    get childrenDepth() {
        return this.props.childrenDepth < 0 ? -1 : Math.max(0, this.props.childrenDepth - 1);
    }

    get menu() {
        let menu = undefined;

        // Check if action is external identifier of menu
        if (typeof this.props.menuId === 'string') {
            menu = this.menuService.getAll().find((item) => item.xmlid === this.props.menuId);
        }

        if (!menu) {
            menu = this.menuService.getMenu(this.props.menuId);
        }

        return menu;
    }

    get counter() {
        return this.menuCounterService.values[this.props.menuId];
    }

    get formattedCounter() {
        return undefined !== this.counter ? humanNumber(this.counter) : undefined;
    }

    toggleChildren() {
        this.setOpened(!this.state.opened);
    }

    setOpened(opened) {
        this.state.opened = this.displayChildren ? !!opened : false;

        if (this.state.opened && this.menu && this.drawerService.closeAllUnactivatedItemsOnOpenMenu) {
            this.drawerService.openMenu(this.menu);
        }
    }

    onItemSelection() {
        if (this.isNextChildrenEnabled) {
            this.toggleSubPanel();
        } else if (this.displayChildren && !this.isPopoverEnabled) {
            this.toggleChildren();
        } else if (this.menu) {
            let menu = this.menu;

            // Force to find first sub menu item with action id
            if (menu && menu.childrenTree.length > 0) {
                menu = findFirstSelectableMenu(menu.childrenTree);
            }

            this.drawerService.selectMenu(menu);
        } else if (this.props.menuAction) {
            this.actionService.doAction(this.props.menuAction, {
                clearBreadcrumbs: true,
            }).then();
        }

        if (this.props.onSelection) {
            this.props.onSelection(this);
        }
    }

    onMenuItemOpened(e) {
        if (this.state.opened && this.drawerService.closeAllUnactivatedItemsOnOpenMenu && !e.detail.ids.includes(this.props.menuId)) {
            this.setOpened(false);
        }
    }

    onMenuItemSelected() {
        if (this.drawerService.closeAllUnactivatedItemsOnClick) {
            this.setOpened(this.menuStateService.menuIsActivated(this.props.menuId));
        }
    }

    onItemMouseEnter() {
        this.openPopover();
    }

    onItemMouseLeave() {
        this.drawerService.popover.close();
    }

    onWillUpdateProps(nextProps) {
        if (nextProps.active && this.drawerService.popover.isOpen) {
            this.openPopover(nextProps);
        }
    }

    openPopover(props) {
        if (this.isPopoverEnabled) {
            this.drawerService.popover.open(this.content.el, {
                ...this.props,
                ...(props || {}),
                displayIcon: false,
                onItemMouseEnter: this.onItemMouseEnter.bind(this),
                onItemMouseLeave: this.onItemMouseLeave.bind(this),
                onItemSelection: this.onItemSelection.bind(this),
                menuItemHref: this.menuItemHref,
            });
        }
    }

    toggleSubPanel() {
        if (this.menu?.id !== this.drawerService.subPanelMenu?.id) {
            this.openSubPanel();
        } else {
            this.closeSubPanel();
        }
    }

    openSubPanel() {
        this.drawerService.openSubPanel(this.menu);
    }

    closeSubPanel() {
        this.drawerService.closeSubPanel();
    }
}
