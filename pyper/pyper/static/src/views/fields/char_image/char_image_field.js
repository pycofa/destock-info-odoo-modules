/** @odoo-module **/

import {registry} from '@web/core/registry';
import {charField, CharField} from '@web/views/fields/char/char_field';

export class CharImageField extends CharField {
    static template = 'pyper.CharImageField';

    static props = {
        ...CharField.props,
        imageWidth: {
            type: Number,
            optional: true,
        },
        imageHeight: {
            type: Number,
            optional: true,
        },
    };
}

export const charImageField = {
    ...charField,
    component: CharImageField,
    extractProps({attrs, options}) {
        return Object.assign(charField.extractProps(...arguments), {
            imageWidth: options.size && Boolean(options.size[0]) ? options.size[0] : attrs.width,
            imageHeight: options.size && Boolean(options.size[1]) ? options.size[1] : attrs.height,
        });
    },
};

registry.category('fields').add('char_image', charImageField);
