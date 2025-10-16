/** @odoo-module **/

export const findFirstSelectableMenu = function (menus) {
    for (const menu of menus) {
        if (menu.childrenTree.length === 0 && menu.actionID) {
            return menu;
        }

        if (menu.childrenTree.length > 0) {
            const result = findFirstSelectableMenu(menu.childrenTree);

            if (result) {
                return result;
            }
        }
    }

    return undefined;
}
