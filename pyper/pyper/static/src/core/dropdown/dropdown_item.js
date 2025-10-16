/** @odoo-module **/

import {DropdownItem} from '@web/core/dropdown/dropdown_item';
import {patch} from '@web/core/utils/patch';

patch(DropdownItem.prototype, {
    get dataAttributes() {
        const attr = super.dataAttributes;
        const styleString = Object.entries(this.props.styles || {})
            .map(([key, value]) => `${key}: ${value};`)
            .join(' ');

        if (styleString) {
            attr['style'] = styleString;
        }

        return attr;
    }
});

DropdownItem.props.styles = {
    type: Object,
    optional: true,
};
