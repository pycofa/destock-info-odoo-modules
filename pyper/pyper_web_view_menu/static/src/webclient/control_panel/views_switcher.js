/** @odoo-module */

import {patch} from '@web/core/utils/patch';
import {ViewsSwitcher} from '@pyper_web_view/search/control_panel/views_switcher';
import {useService} from '@web/core/utils/hooks';

patch(ViewsSwitcher.prototype, {
    setup() {
        super.setup();
        this.menuService = useService('menu');
    },

    get viewsFields() {
        return [...super.viewsFields, 'bookmarked'];
    },

    get viewModeIcons() {
        return {
            ...super.viewModeIcons,
            'tree': 'ph ph-table',
            'kanban': 'ph ph-kanban',
        }
    },

    async bookmarkView(view) {
        await this.actionService.doActionButton({
            resModel: 'ir.views',
            resId: view.id,
            type: 'object',
            name: 'bookmark',
            args: JSON.stringify([this.getViewIcon(view.view_mode)]),
        });
        view.bookmarked = true;
    },

    async unbookmarkView(view) {
        await this.actionService.doActionButton({
            resModel: 'ir.views',
            resId: view.id,
            type: 'object',
            name: 'unbookmark',
        });
        view.bookmarked = false;
        await this._validateSelectedMenu(view);
    },

    async _onViewDeleted(view) {
        await super._onViewDeleted(view);
        await this._validateSelectedMenu(view);
    },

    async _validateSelectedMenu(view) {
        if (view['ir_action_id'] && view['ir_action_id'][0] && view['ir_action_id'][0] === this.env?.config?.actionId) {
            const rootMenu = await this.menuService.getMenuAsTree('root');
            const menu = findFirstMenuItemWithAction(rootMenu.childrenTree || []);

            if (menu) {
                await this.menuService.selectMenu(menu);
            }
        }
    },
});

function findFirstMenuItemWithAction(menuItems) {
    for (const menuItem of menuItems) {
        if (menuItem.actionID) {
            return menuItem;
        }

        if (menuItem.childrenTree && menuItem.childrenTree.length > 0) {
            const found = findFirstMenuItemWithAction(menuItem.childrenTree);

            if (found) {
                return found;
            }
        }
    }

    return null;
}
