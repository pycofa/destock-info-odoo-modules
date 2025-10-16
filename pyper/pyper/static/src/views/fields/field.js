/** @odoo-module */

import {patch} from '@web/core/utils/patch';
import {Field} from '@web/views/fields/field';
import {pick} from '@web/core/utils/objects';

patch(Field.prototype, {
    async onJsEvent(event) {
        const code = event.code ? event.code.toLowerCase() : undefined;

        if (this.props.fieldInfo.jsOn[event.type] && this.props.fieldInfo.jsOn[event.type][code]) {
            const value = this.props.fieldInfo.jsOn[event.type][code];
            const parts = value.split(':');
            let method = parts[0];
            let type = 'controller';

            if (parts.length > 1) {
                type = parts[0];
                method = parts[1];
            }

            if (['object', 'action'].includes(type)) {
                await this.env.onClickViewButton({
                    clickParams: {
                        name: method,
                        type: type,
                    },
                    getResParams: () => pick(
                        this.props.record.model.root,
                        'context',
                        'evalContext',
                        'resModel',
                        'resId',
                        'resIds',
                    ),
                });
            } else {
                this.props.record.model.bus.trigger('JS_ON_EVENT', method);
            }
        }
    },
});

patch(Field, {
    parseFieldNode(node, models, modelName, viewType, jsClass) {
        const fieldInfo = super.parseFieldNode(node, models, modelName, viewType, jsClass);
        const attrKeys = Object.keys(fieldInfo.attrs);

        fieldInfo.jsOn = {};

        attrKeys.forEach((attr) => {
            if (attr.startsWith('js_on_')) {
                const [eventName, eventCode] = attr.substring(6).split('.');
                fieldInfo.jsOn[eventName] = fieldInfo.jsOn[eventName] || {};
                fieldInfo.jsOn[eventName][eventCode] = fieldInfo.attrs[attr];

                delete fieldInfo.attrs[attr];
            }
        });

        return fieldInfo;
    },
});
