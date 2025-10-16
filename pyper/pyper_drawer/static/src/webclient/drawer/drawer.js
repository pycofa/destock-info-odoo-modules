/** @odoo-module **/

import {
    Component,
    onMounted,
    onWillDestroy,
    onWillStart,
    onWillUpdateProps,
    onPatched,
    useRef,
    useEffect,
    useExternalListener,
    useState,
} from '@odoo/owl';
import {useBus, useService} from '@web/core/utils/hooks';
import {debounce} from '@web/core/utils/timing';
import {DropdownItem} from '@web/core/dropdown/dropdown_item';
import {getTransform, stylesToString} from '@pyper/core/ui/css';
import {DrawerMenuItem} from './drawer_menu_item';
import {DrawerSubPanel} from './drawer_sub_panel';


export class Drawer extends Component {
    static template = 'pyper_drawer.Drawer';

    static components = {
        DropdownItem,
        DrawerMenuItem,
        DrawerSubPanel,
    };

    static props = {
        showRootApp: {
            type: Boolean,
            optional: true,
        },
        fixedTop: {
            type: Boolean,
            optional: true,
        },
        nav: {
            type: Boolean,
            optional: true,
        },
        alwaysHeader: {
            type: Boolean,
            optional: true,
        },
        alwaysFooter: {
            type: Boolean,
            optional: true,
        },
        alwaysMini: {
            type: Boolean,
            optional: true,
        },
        minifiable: {
            type: Boolean,
            optional: true,
        },
        initMinified: {
            type: Boolean,
            optional: true,
        },
        initLockable: {
            type: Boolean,
            optional: true,
        },
        popoverMinified: {
            type: Boolean,
            optional: true,
        },
        closeAction: {
            type: Boolean,
            optional: true,
        },
        closeOnClick: {
            type: Boolean,
            optional: true,
        },
        closeAllUnactivatedItemsOnOpenMenu: {
            type: Boolean,
            optional: true,
        },
        closeAllUnactivatedItemsOnClick: {
            type: Boolean,
            optional: true,
        },
        subItemsDepth: {
            type: Number,
            optional: true,
        },
        nextItemsSubPanel: {
            type: Boolean,
            optional: true,
        },
        dragEndRatio: {
            type: Number,
            optional: true,
        },
        hideEmptyCategory: {
            type: Boolean,
            optional: true,
        },
        hideCategoryLabelFull: {
            type: Boolean,
            optional: true,
        },
        hideCategoryLabelMinified: {
            type: Boolean,
            optional: true,
        },
        showCategorySectionMinified: {
            type: Boolean,
            optional: true,
        },
        disabledOnSmallScreen: {
            type: Boolean,
            optional: true,
        },
        hideNavbarAppsMenu: {
            type: Boolean,
            optional: true,
        },
        slots: {
            type: Object,
            optional: true,
        },
    };

    static defaultProps = {
        showRootApp: undefined,
        nav: undefined,
        fixedTop: undefined,
        alwaysHeader: undefined,
        alwaysFooter: undefined,
        alwaysMini: undefined,
        minifiable: undefined,
        initMinified: undefined,
        initLockable: undefined,
        popoverMinified: undefined,
        closeAction: undefined,
        closeOnClick: undefined,
        closeAllUnactivatedItemsOnOpenMenu: undefined,
        closeAllUnactivatedItemsOnClick: undefined,
        subItemsDepth: undefined,
        nextItemsSubPanel: undefined,
        dragEndRatio: undefined,
        hideEmptyCategory: undefined,
        hideCategoryLabelFull: undefined,
        hideCategoryLabelMinified: undefined,
        showCategorySectionMinified: undefined,
        disabledOnSmallScreen: undefined,
        hideNavbarAppsMenu: undefined,
    };

    static configurableMenuDefaultProps = {
        preferWebIcon: false,
    };

    static configurableDefaultProps = {
        showRootApp: false,
        nav: false,
        fixedTop: false,
        alwaysHeader: false,
        alwaysFooter: false,
        alwaysMini: false,
        minifiable: false,
        initMinified: false,
        initLockable: true,
        popoverMinified: false,
        closeAction: false,
        closeOnClick: false,
        closeAllUnactivatedItemsOnOpenMenu: true,
        closeAllUnactivatedItemsOnClick: false,
        subItemsDepth: 0,
        nextItemsSubPanel: false,
        dragEndRatio: 0.25,
        hideEmptyCategory: false,
        hideCategoryLabelFull: false,
        hideCategoryLabelMinified: false,
        showCategorySectionMinified: false,
        disabledOnSmallScreen: false,
        hideNavbarAppsMenu: false,
    };

    static MENU_SETUP_PREFIX = 'pyper_menu.provider.';

    static SETUP_PREFIX = 'pyper_drawer.drawer_props.';

    setup() {
        this.rpc = useService('rpc');
        this.pyperSetupService = useService('pyper_setup');
        this.drawerService = useState(useService('drawer'));
        this.actionService = useState(useService('action'));
        this.menuService = useService('menu');
        this.root = useRef('root');
        this.appSubMenus = useRef('appSubMenus');
        this.dragScrollables = undefined;
        this.dragScrolling = undefined;
        this.dragStartX = undefined;
        this.dragStartPosition = undefined;
        this.dragMaxWidth = undefined;
        this.dragDistance = 0;

        onWillStart(async () => {
            await this.pyperSetupService.register(Drawer.MENU_SETUP_PREFIX, Drawer.configurableMenuDefaultProps);
            await this.pyperSetupService.register(Drawer.SETUP_PREFIX, Drawer.configurableDefaultProps);
            this._refreshDrawerService();
        });

        const debouncedAdapt = debounce(this.adapt.bind(this), 250);
        onWillDestroy(() => {
            this.pyperSetupService.unregister(Drawer.MENU_SETUP_PREFIX);
            this.pyperSetupService.unregister(Drawer.SETUP_PREFIX);
            debouncedAdapt.cancel();

            const menuEl = document.querySelector('.o_navbar .o_main_navbar .o_navbar_apps_menu');

            if (menuEl) {
                menuEl.classList.remove('o_navbar_apps_menu--hide');
            }
        });
        useExternalListener(window, 'resize', debouncedAdapt);

        let adaptCounter = 0;
        const renderAndAdapt = () => {
            adaptCounter++;
            this.render();
        };

        useBus(this.env.bus, 'MENUS:APP-CHANGED', renderAndAdapt);
        useBus(this.env.bus, 'DRAWER:TOGGLE', this.toggle);
        useBus(this.env.bus, 'DRAWER:SELECT-MENU', (evt) => {
            this.selectMenu(evt.detail);
        });
        useBus(this.env.bus, 'MENU-STATE:MENU-SELECTED', (e) => {
            // Force to mount the drawer if onPatched is not executed because selected menu does not exist
            // in initialization
            if (!this.drawerService.mounted) {
                this.drawerService.mounted = true;
            }
        });

        onMounted(() => {
            this.onWillUpdateProps(this.props);

            if (this.settings.hideNavbarAppsMenu) {
                const menuEl = document.querySelector('.o_navbar .o_main_navbar .o_navbar_apps_menu');

                if (menuEl) {
                    menuEl.classList.add('o_navbar_apps_menu--hide');
                }
            }
        });

        onPatched(() => {
            if (!this.drawerService.mounted) {
                this.drawerService.mounted = true;
            }
        });

        useEffect(
            () => {
                this.adapt().then();
            },
            () => [adaptCounter]
        );

        // Init and refresh values of drawer service
        onWillUpdateProps((nextProps) => this.onWillUpdateProps(nextProps));
    }

    get settings() {
        return {
            ...this.pyperSetupService.settings[Drawer.MENU_SETUP_PREFIX],
            ...this.pyperSetupService.settings[Drawer.SETUP_PREFIX],
        };
    }

    get classes() {
        return {
            'o_drawer': true,
            'o_drawer--ready': this.isMounted,
            'o_drawer--opened': this.isOpened,
            'o_drawer--locked': this.isLocked,
            'o_drawer--mini': this.isMinified,
            'o_drawer--always-mini': this.drawerService.alwaysMinified,
            'o_drawer--popover-items': this.drawerService.isPopoverMinified,
            'o_drawer--nav': this.isNav,
            'o_drawer--fixed-top': this.isFixedTop,
            'o_drawer--hoverable': this.isHoverable,
            'o_drawer--dragging': this.isDragging,
            'o_drawer--sub-panel--opened': this.isSubPanelOpened,
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

    get isSmallScreen() {
        return this.drawerService.isSmallScreen;
    }

    get isLockable() {
        return this.drawerService.isLockable;
    }

    get isLocked() {
        return this.drawerService.isLocked;
    }

    get isMinifiable() {
        return this.drawerService.isMinifiable;
    }

    get isMinified() {
        return this.drawerService.isMinified;
    }

    get isHoverable() {
        return this.drawerService.isHoverable;
    }

    get isDraggable() {
        return this.drawerService.isDraggable;
    }

    get isDragging() {
        return this.drawerService.dragging;
    }

    get isOpened() {
        return this.drawerService.isOpened;
    }

    get isSubPanelOpened() {
        return this.drawerService.isSubPanelOpened;
    }

    get isClosed() {
        return this.drawerService.isClosed;
    }

    get isNav() {
        return this.drawerService.isNav;
    }

    get isFixedTop() {
        return this.drawerService.isFixedTop;
    }

    get appName() {
        return this.pyperSetupService.appName;
    }

    get headerBadgeUrl() {
        return this.drawerService.headerBadgeUrl;
    }

    get displayCategoryName() {
        return (!this.isMinified && !this.settings.hideCategoryLabelFull)
            ||
            (this.isMinified && !this.settings.hideCategoryLabelMinified)
        ;
    }

    get displayCategorySection() {
        return this.isMinified && this.settings.hideCategoryLabelMinified && this.settings.showCategorySectionMinified;
    }

    get displayQuickActions() {
        return !!this.mainQuickAction;
    }

    get displayHeader() {
        return this.isSmallScreen || this.settings.alwaysHeader;
    }

    get displayFooter() {
        return this.isSmallScreen || this.settings.alwaysFooter;
    }

    get currentApp() {
        return this.menuService.getCurrentApp();
    }

    get currentAppSections() {
        const currentId = this.currentApp && !this.settings.showRootApp ? this.currentApp.id : 'root';
        const menu = this.menuService.getMenuAsTree(currentId);

        return menu.childrenTree || [];
    }

    get mainCategoryAppSections() {
        const categories = {};

        this.currentAppSections.forEach((menu) => {
            if (menu.position) {
                return;
            }

            const menuCatId = menu.category ? menu.category[0] : undefined;
            const menuCatName = menu.category ? menu.category[1] : undefined;
            const menuCatSeq = menu.categorySequence ? menu.categorySequence : undefined;
            const menuCatIcon = menu.categoryFontIcon ? menu.categoryFontIcon : undefined;
            const menuCatIconColor = menu.categoryFontIconColor ? menu.categoryFontIconColor : undefined;
            const menuCatActionId = menu.categoryActionId ? menu.categoryActionId : undefined;

            if (undefined === categories[menuCatId]) {
                categories[menuCatId] = {
                    label: menuCatName || undefined,
                    sequence: menuCatSeq,
                    value: menuCatId || 0,
                    fontIcon: menuCatIcon,
                    fontIconColor: menuCatIconColor,
                    actionID: menuCatActionId,
                    menus: [],
                }
            }

            categories[menuCatId]['menus'].push(menu);
        });

        if (this.settings.hideEmptyCategory) {
            delete categories[undefined];
        }

        const categoryList = Object.keys(categories).map(key => categories[key]);
        categoryList.sort((a, b) => {
            if (a.sequence === undefined) {
                return -1;
            }

            if (b.sequence === undefined) {
                return 1;
            }

            return a.sequence - b.sequence;
        });

        return categoryList;
    }

    get mainStartChildrenDepth() {
        if (this.isMinifiable && this.isMinified && this.drawerService.nextItemsSubPanel) {
            return 0;
        }

        return this.settings.subItemsDepth < 0 ? -1 : Math.max(0, this.settings.subItemsDepth);
    }

    get quickActionSections() {
        const menus = [];

        this.currentAppSections.forEach((menu) => {
            if ('drawer_quick_actions' === menu.position) {
                menus.push(menu);
            }
        });

        return menus;
    }

    get mainQuickAction() {
        return this.quickActionSections.length > 0 ? this.quickActionSections[0] : undefined;
    }

    get secondaryQuickActions() {
        return this.quickActionSections.length > 1 ? this.quickActionSections.slice(1) : [];
    }

    get footerAppSections() {
        const menus = [];

        this.currentAppSections.forEach((menu) => {
            if ('drawer_footer' === menu.position) {
                menus.push(menu);
            }
        });

        return menus;
    }

    open() {
        if (this.isSmallScreen) {
            if (!this.isOpened && !this.settings.disabledOnSmallScreen) {
                this.drawerService.opened = true;
                this.root.el.style.transform = '';
            }
        } else {
            if (this.isLockable && !this.isLocked) {
                this.drawerService.locked = true;
            } else if (!this.isLockable && !this.isOpened) {
                this.drawerService.opened = true;
            }

            this.root.el.style.transform = '';

            debounce(() => window.dispatchEvent(new CustomEvent('resize')), 1)();
        }
    }

    close() {
        if (this.isSmallScreen) {
            if (this.isOpened) {
                this.drawerService.opened = false;
                this.root.el.style.transform = '';
            }
        } else {
            if (this.isLockable && this.isLocked) {
                this.drawerService.locked = false;
            } else if (!this.isLockable && this.isOpened) {
                this.drawerService.opened = false;
            }

            this.root.el.style.transform = '';

            debounce(() => window.dispatchEvent(new CustomEvent('resize')), 1)();
        }

        this.drawerService.closeSubPanel();
    }

    toggle() {
        if (this.isSmallScreen) {
            if (this.isOpened) {
                this.close();
            } else {
                this.open();
            }
        } else {
            if (this.isLockable && this.isLocked) {
                this.close();
            } else if (this.isLockable && !this.isLocked) {
                this.open();
            } else if (!this.isLockable && this.isOpened) {
                this.close();
            } else if (!this.isLockable && !this.isOpened) {
                this.open();
            } else if (this.isOpened) {
                this.close();
            } else {
                this.open();
            }
        }
    }

    async adapt() {
        if (!this.root.el) {
            // currently, the promise returned by 'render' is resolved at the end of
            // the rendering even if the component has been destroyed meanwhile, so we
            // may get here and have this.el unset
            return;
        }

        // ------- Initialize -------
        // Get the sectionsMenu
        const sectionsMenu = this.appSubMenus.el;
        if (!sectionsMenu) {
            // No need to continue adaptations if there is no sections menu.
            return;
        }

        return this.render();
    }

    selectMenu(menu) {
        if (menu) {
            this.menuService.selectMenu(menu).then();
            this.drawerService.closeSubPanel();

            if (this.settings.closeOnClick && this.drawerService.isClosable) {
                this.close();
            }
        }
    }

    onWillUpdateProps(nextProps) {
        this.pyperSetupService.onWillUpdateProps(Drawer.MENU_SETUP_PREFIX, nextProps);
        this.pyperSetupService.onWillUpdateProps(Drawer.SETUP_PREFIX, nextProps);
        this._refreshDrawerService();
    }

    async onClickQuickAction(menu) {
        await this.actionService.doAction(menu.actionID, {
            clearBreadcrumbs: true,
        });
    }

    async onClickCategoryAction(category) {
        await this.actionService.doAction(category.actionID, {
            clearBreadcrumbs: true,
            additionalContext: {
                active_id: category.value,
                active_ids: [category.values],
                active_model: 'ir.ui.menu.category',
            }
        });
    }

    _onTouchStartDrag(ev) {
        if (!this.isDraggable || (this.isSmallScreen && this.settings.disabledOnSmallScreen)) {
            return;
        }

        this.dragScrollables = ev
            .composedPath()
            .filter(
                (e) => {
                    const valid = e.nodeType === 1
                        && (this.root.el.contains(e) || e === this.root.el)
                        && e.scrollHeight > e.getBoundingClientRect().height
                        && ['auto', 'scroll'].includes(window.getComputedStyle(e)['overflow-y']);

                    if (valid) {
                        e.addEventListener('scroll', this._onTouchScroll.bind(this));
                    }

                    return valid;
                }
            );

        this.drawerService.dragging = true;
        this.dragStartX = ev.touches[0].clientX;
        this.dragStartPosition = getTransform(this.root.el, true).e;
        this.dragMaxWidth = this.root.el.getBoundingClientRect().width;
        this.dragDistance = 0;
        this.root.el.style.transition = 'none';
    }

    /**
     * @private
     * @param {TouchEvent} ev
     */
    _onTouchMoveDrag(ev) {
        if (!this.isDraggable || !this.isDragging) {
            return;
        }

        this.dragDistance = Math.round(ev.touches[0].clientX - this.dragStartX);
        let translateX = this.dragStartPosition + this.dragDistance;
        translateX = Math.max(translateX, -this.dragMaxWidth);
        translateX = Math.min(translateX, 0);

        if (this.dragScrolling) {
            return;
        }

        if (this.drawerService.isSubPanelOpened) {
            this.drawerService.closeSubPanel();
        }

        this.root.el.style.transform = `translateX(${translateX}px)`;
    }

    /**
     * @private
     * @param {TouchEvent} ev
     */
    _onTouchEndDrag(ev) {
        if (!this.isDraggable || !this.isDragging) {
            return;
        }

        this.dragScrollables.forEach((e) => {
            e.removeEventListener('scroll', this._onTouchScroll.bind(this));
        });

        const dragDistance = this.dragDistance;
        const dragMaxWidth = this.dragMaxWidth;
        const dragActionable = !this.dragScrolling;

        this.drawerService.dragging = false;
        this.dragScrollables = undefined;
        this.dragScrolling = undefined;
        this.dragStartX = undefined;
        this.dragStartPosition = undefined;
        this.dragMaxWidth = undefined;
        this.dragDistance = 0;
        this.root.el.style.transition = '';

        if (dragActionable && Math.abs(dragDistance) >= (dragMaxWidth * this.settings.dragEndRatio)) {
            if (this.isOpened) {
                this.close();
            } else if (this.isClosed) {
                this.open();
            }
        }

        this.root.el.style.transform = '';
    }

    _onTouchScroll() {
        this.dragScrolling = true;
    }

    _refreshDrawerService() {
        this.drawerService.nav = this.settings.nav;
        this.drawerService.fixedTop = this.settings.fixedTop;
        this.drawerService.alwaysMinified = this.settings.alwaysMini;
        this.drawerService.minifiable = this.settings.minifiable;
        this.drawerService.popoverMinified = this.settings.popoverMinified;
        this.drawerService.nextItemsSubPanel = this.settings.nextItemsSubPanel;
        this.drawerService.disabledOnSmallScreen = this.settings.disabledOnSmallScreen;
        this.drawerService.closeAllUnactivatedItemsOnOpenMenu = this.settings.closeAllUnactivatedItemsOnOpenMenu;
        this.drawerService.closeAllUnactivatedItemsOnClick = this.settings.closeAllUnactivatedItemsOnClick;
        this.drawerService.restoreMinified(this.settings.initMinified);
        this.drawerService.restoreLockable(this.settings.initLockable);
        this.drawerService.neutralizeBannerTop = document.getElementById('oe_neutralize_banner')?.getBoundingClientRect()?.height || 0;
    }
}
