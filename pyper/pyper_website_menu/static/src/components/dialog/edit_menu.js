/** @odoo-module */

import {EditMenuDialog, MenuDialog} from '@website/components/dialog/edit_menu';

import {patch} from '@web/core/utils/patch';
import {useEffect, useState} from '@odoo/owl';

const useControlledInput = (initialValue, validate) => {
    const input = useState({
        value: initialValue,
        hasError: false,
    });

    const isValid = () => {
        if (validate(input.value)) {
            return true;
        }
        input.hasError = true;
        return false;
    };

    useEffect(() => {
        input.hasError = false;
    }, () => [input.value]);

    return {
        input,
        isValid,
    };
};

patch(MenuDialog.prototype, {
    setup() {
        super.setup();
        this.structuredMenuColumns = useControlledInput(this.props.structuredMenuColumns, value => value);
        this.structuredMenuObfuscator = useControlledInput(this.props.structuredMenuObfuscator, value => !!value);
        this.description = useControlledInput(this.props.description, value => value);
        this.fontIcon = useControlledInput(this.props.fontIcon, value => value);
        this.fontIconColor = useControlledInput(this.props.fontIconColor, value => value);
    },

    onClickOk() {
        if (this.name.isValid() && (this.props.isStructuredMenu || this.props.parentIsStructuredMenu)) {
            this.props.save(
                this.name.input.value,
                this.url.input.value,
                this.structuredMenuColumns.input.value,
                this.structuredMenuObfuscator.input.value,
                this.description.input.value,
                this.fontIcon.input.value,
                this.fontIconColor.input.value
            );
            this.props.close();
        } else {
            super.onClickOk();
        }
    },
});

MenuDialog.props.isStructuredMenu = {type: Boolean, optional: true};
MenuDialog.props.structuredMenuColumns = {type: Number, optional: true};
MenuDialog.props.structuredMenuObfuscator = {type: Number, optional: true};
MenuDialog.props.parentIsStructuredMenu = {type: Boolean, optional: true};
MenuDialog.props.description = {type: String, optional: true};
MenuDialog.props.fontIcon = {type: String, optional: true};
MenuDialog.props.fontIconColor = {type: String, optional: true};

patch(EditMenuDialog.prototype, {
    addStructuredMenu() {
        this.dialogs.add(MenuDialog, {
            isMegaMenu: true, // Only to hide fields
            isStructuredMenu: true,
            save: (name, url, isNewWindow) => {
                const newMenu = {
                    fields: {
                        id: `menu_${(new Date).toISOString()}`,
                        name,
                        url: '#',
                        new_window: isNewWindow,
                        'is_structured_menu': true,
                        sequence: 0,
                        'parent_id': false,
                    },
                    'children': [],
                };
                this.map.set(newMenu.fields['id'], newMenu);
                this.state.rootMenu.children.push(newMenu);
            },
        });
    },

    editMenu(id) {
        const menuToEdit = this.map.get(id);
        const isStructuredMenu = menuToEdit.fields['is_structured_menu']
        const parentIsStructuredMenu = menuToEdit.fields['parent_is_structured_menu']

        if (isStructuredMenu || parentIsStructuredMenu) {
            this.dialogs.add(MenuDialog, {
                name: menuToEdit.fields['name'],
                url: menuToEdit.fields['url'],
                isStructuredMenu: isStructuredMenu,
                structuredMenuColumns: menuToEdit.fields['structured_menu_columns'],
                structuredMenuObfuscator: menuToEdit.fields['structured_menu_obfuscator'],
                parentIsStructuredMenu: parentIsStructuredMenu,
                description: menuToEdit.fields['description'],
                fontIcon: menuToEdit.fields['font_icon'],
                fontIconColor: menuToEdit.fields['font_icon_color'],
                save: (name, url, structuredMenuColumns, structuredMenuObfuscator, description, fontIcon, fontIconColor) => {
                    menuToEdit.fields['name'] = name;
                    menuToEdit.fields['url'] = url;
                    menuToEdit.fields['structured_menu_columns'] = structuredMenuColumns;
                    menuToEdit.fields['structured_menu_obfuscator'] = structuredMenuObfuscator;
                    menuToEdit.fields['description'] = description;
                    menuToEdit.fields['font_icon'] = fontIcon;
                    menuToEdit.fields['font_icon_color'] = fontIconColor;
                },
            });
        } else {
            super.editMenu(id);
        }
    },

    _moveMenu({element, parent}) {
        super._moveMenu(...arguments);

        // Define parent_is_structured_menu value when item is moved
        const menuId = this._getMenuIdForElement(element);
        const menu = this.map.get(menuId);

        const parentId = menu.fields['parent_id'] || this.state.rootMenu.fields['id'];
        let parentMenu = this.map.get(parentId);

        menu.fields['parent_is_structured_menu'] = !!parentMenu.fields['is_structured_menu'];
    },

    _isAllowedMove(current, elementSelector) {
        // Allow move structured menu item only in root level
        if (current.element.dataset.isStructuredMenu === 'true') {
            return current.placeHolder.parentNode.closest(elementSelector) === null;
        }

        return super._isAllowedMove(current, elementSelector);
    },
});
