/** @odoo-module **/

import {reactive} from '@odoo/owl';
import {cookie} from '@web/core/browser/cookie';
import {registry} from '@web/core/registry';
import {SIZES} from '@web/core/ui/ui_service';


export class DrawerState {
    constructor(envBus, ui, menuState) {
        this.envBus = envBus;
        /** @type {import("@web/core/ui/ui_service").uiService} */
        this.uiService = ui;
        /** @type {import("@pyper/webclient/menus/menu_state_service").menuStateService} */
        this.menuStateService = menuState;
    }

    setup() {
        this.state = {
            nav: false,
            fixedTop: false,
            neutralizeBannerTop: 0,
            opened: false,
            locked: (cookie.get('drawer_locked') || 'true') === 'true',
            lockable: false,
            minifiable: false,
            minified: false,
            alwaysMinified: false,
            popoverMinified: false,
            disabledOnSmallScreen: false,
            nextItemsSubPanel: false,
            dragging: false,
            mounted: false,
            closeAllUnactivatedItemsOnOpenMenu: false,
            closeAllUnactivatedItemsOnClick: false,
            subPanelOpened: false,
            subPanelMenu: null,
            headerBadgeUrl: null,
        };
    }

    get nav() {
        return this.state.nav;
    }

    set nav(nav) {
        this.state.nav = nav;
    }

    get fixedTop() {
        return this.state.fixedTop;
    }

    set fixedTop(fixedTop) {
        this.state.fixedTop = fixedTop;
    }

    get opened() {
        return this.state.opened;
    }

    set opened(opened) {
        this.state.opened = opened;
    }

    get locked() {
        return this.state.locked;
    }

    set locked(locked) {
        this.state.locked = locked;
        cookie.set('drawer_locked', locked);
    }

    get lockable() {
        return this.state.lockable;
    }

    set lockable(lockable) {
        if (lockable && this.state.opened && !this.isSmallScreen) {
            this.state.opened = false;
        } else if (!lockable && !this.state.opened && !this.isSmallScreen) {
            this.state.opened = true;
        }

        this.state.lockable = lockable;
        cookie.set('drawer_lockable', lockable);
    }

    get minifiable() {
        return this.state.minifiable;
    }

    set minifiable(minifiable) {
        this.state.minifiable = minifiable;
    }

    get minified() {
        return this.state.minified;
    }

    set minified(minified) {
        this.closeSubPanel();
        this.state.minified = minified;
        cookie.set('drawer_minified', minified);
    }

    get alwaysMinified() {
        return this.state.alwaysMinified;
    }

    set alwaysMinified(alwaysMinified) {
        this.state.alwaysMinified = alwaysMinified;
    }

    get popoverMinified() {
        return this.state.popoverMinified;
    }

    set popoverMinified(popoverMinified) {
        this.state.popoverMinified = popoverMinified;
    }

    get nextItemsSubPanel() {
        return this.state.nextItemsSubPanel;
    }

    set nextItemsSubPanel(nextItemsSubPanel) {
        this.state.nextItemsSubPanel = nextItemsSubPanel;
    }

    get disabledOnSmallScreen() {
        return this.state.disabledOnSmallScreen;
    }

    set disabledOnSmallScreen(disabledOnSmallScreen) {
        this.state.disabledOnSmallScreen = disabledOnSmallScreen;
    }

    get dragging() {
        return this.state.dragging;
    }

    set dragging(dragging) {
        this.state.dragging = dragging;
    }

    get mounted() {
        return this.state.mounted;
    }

    set mounted(mounted) {
        this.state.mounted = mounted;
    }

    get isSmallScreen() {
        return this.uiService.size <= SIZES.LG;
    }

    get isNav() {
        return this.nav;
    }

    get isLockable() {
        return this.lockable;
    }

    get isLocked() {
        return this.locked && this.isLockable && !this.isSmallScreen;
    }

    get isMinifiable() {
        return this.minifiable || this.alwaysMinified;
    }

    get isMinified() {
        return (this.minified || this.alwaysMinified) && this.isMinifiable && !this.isSmallScreen && this.isLocked;
    }

    get isPopoverMinified() {
        return this.isMinified && this.popoverMinified;
    }

    get isHoverable() {
        return this.isSmallScreen || !this.locked;
    }

    get isDraggable() {
        return this.isHoverable;
    }

    get isOpened() {
        return this.opened;
    }

    get isClosed() {
        return !this.opened;
    }

    get isClosable() {
        return !this.isLocked && this.opened;
    }

    get isFixedTop() {
        return this.fixedTop && !this.isSmallScreen;
    }

    get popover() {
        return this._popover;
    }

    set popover(popover) {
        this._popover = popover;
    }

    get closeAllUnactivatedItemsOnOpenMenu() {
        return this.state.closeAllUnactivatedItemsOnOpenMenu;
    }

    set closeAllUnactivatedItemsOnOpenMenu(value) {
        this.state.closeAllUnactivatedItemsOnOpenMenu = value;
    }

    get closeAllUnactivatedItemsOnClick() {
        return this.state.closeAllUnactivatedItemsOnClick;
    }

    set closeAllUnactivatedItemsOnClick(value) {
        this.state.closeAllUnactivatedItemsOnClick = value;
    }

    get subPanelOpened() {
        return this.state.subPanelOpened;
    }

    get subPanelMenu() {
        return this.state.subPanelMenu;
    }

    get isSubPanelOpened() {
        return (this.isOpened || this.isLocked) && this.subPanelOpened;
    }

    get headerBadgeUrl() {
        if (!this.state.headerBadgeUrl) {
            this.state.headerBadgeUrl = document.querySelector('link[type="image/x-icon"]')
                ?.getAttribute('href');
        }

        return this.state.headerBadgeUrl;
    }

    restoreMinified(defaultMinified) {
        defaultMinified = ['true', true].includes(defaultMinified);
        const defaultValue = defaultMinified ? 'true' : 'false';
        const minified = (cookie.get('drawer_minified') || defaultValue) === 'true';

        this.state.minified = minified;

        return minified;
    }

    restoreLockable(defaultLockable) {
        defaultLockable = ['true', true].includes(defaultLockable);
        const defaultValue = defaultLockable ? 'true' : 'false';
        const lockable = (cookie.get('drawer_lockable') || defaultValue) === 'true';

        this.state.lockable = lockable;

        return lockable;
    }

    toggle() {
        this.envBus.trigger('DRAWER:TOGGLE');
    }

    selectMenu(menu) {
        this.envBus.trigger('DRAWER:SELECT-MENU', menu);
    }

    openMenu(menu) {
        if (menu) {
            const parentIds = this.menuStateService.findParentIds(menu.id);
            const ids = [menu.id, ...parentIds];

            if (!this.menuStateService.findAllChildrenIds(this.subPanelMenu?.id).includes(menu.id)) {
                this.closeSubPanel();
            }

            this.envBus.trigger('DRAWER:OPEN-MENU', {menu, ids});
        }
    }

    openSubPanel(menu) {
        if (menu) {
            this.state.subPanelOpened = true;
            this.state.subPanelMenu = menu;
        } else {
            this.closeSubPanel();
        }
    }

    closeSubPanel() {
        this.state.subPanelOpened = false;
        this.state.subPanelMenu = null;
    }
}

export const drawerService = {
    dependencies: ['ui', 'menu_state'],
    start(env, {ui, menu_state}) {
        const drawerState = reactive(new DrawerState(env.bus, ui, menu_state));
        drawerState.setup();

        return drawerState;
    },
};

registry.category('services').add('drawer', drawerService);
