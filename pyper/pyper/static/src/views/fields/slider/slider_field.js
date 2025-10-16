/** @odoo-module */

import {Component} from '@odoo/owl';
import {registry} from '@web/core/registry';
import {standardFieldProps} from '@web/views/fields/standard_field_props';
import {useInputField} from '@web/views/fields/input_field_hook';

export class SliderField extends Component {
    static template = 'pyper.SliderField';

    static props = {
        ...standardFieldProps,
        step: {type: [Number, String], optional: true},
        min: {type: [Number, String], optional: true},
        max: {type: [Number, String], optional: true},
    };

    static defaultProps = {
        step: 1,
        min: 0,
        max: 100,
    };

    setup() {
        useInputField({
            getValue: () => {
                return this.props.record.data[this.props.name] || 0;
            },
        });
    }
}

export const slider = {
    component: SliderField,
    displayName: 'Slider',
    supportedTypes: ['integer'],
    extractProps: ({attrs, options}) => ({
        step: attrs.step,
        min: attrs.min,
        max: attrs.max,
    }),
};

registry.category('fields').add('slider', slider);
