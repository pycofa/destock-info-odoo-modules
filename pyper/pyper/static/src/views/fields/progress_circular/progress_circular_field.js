/** @odoo-module */

import {Component} from '@odoo/owl';
import {registry} from '@web/core/registry';
import {standardFieldProps} from '@web/views/fields/standard_field_props';
import {stylesToString} from '@pyper/core/ui/css';

export class ProgressCircular extends Component {
    static template = 'pyper.ProgressCircular';

    static props = {
        ...standardFieldProps,
        min: {type: [Number, String], optional: true},
        max: {type: [Number, String], optional: true},
        width: {type: [Number, String], optional: true},
        size: {type: [Number, String], optional: true},
        rotate: {type: [Number, String], optional: true},
        color: {type: [String], optional: true},
        indeterminate: {type: [Boolean, String], optional: true, validate: v => [true, false, 'disable-shrink'].includes(v)},
        displayValue: {type: [Boolean], optional: true},
        hideEmpty: {type: [Boolean], optional: true},
    };

    static defaultProps = {
        min: 0,
        max: 100,
        width: 4,
        size: 'default',
        rotate: 0,
        color: 'primary',
        indeterminate: false,
        displayValue: false,
        hideEmpty: false,
    };

    static PREDEFINED_SIZES = ['x-small', 'small', 'default', 'large', 'x-large']

    static MAGIC_RADIUS_CONSTANT = 20;

    static CIRCUMFERENCE = 2 * Math.PI * ProgressCircular.MAGIC_RADIUS_CONSTANT;

    get value() {
        return this.props.record.data[this.props.name];
    }

    get formattedValue() {
        return this.value === false ? undefined : this.value;
    }

    get normalizedValue() {
        const value = ((this.value / this.props.max) * 100);

        return Math.max(0, Math.min(100, value));
    };

    get isEmpty() {
        return this.props.hideEmpty && typeof this.value !== 'number' && this.props.indeterminate === false;
    }

    get sizeValue() {
        return ProgressCircular.PREDEFINED_SIZES.includes(this.props.size) ? 32 : this.props.size;
    }

    get diameter() {
        return (ProgressCircular.MAGIC_RADIUS_CONSTANT / (1 - this.props.width / this.sizeValue)) * 2;
    }

    get magicRadiusConstant() {
        return ProgressCircular.MAGIC_RADIUS_CONSTANT;
    }

    get strokeWidth() {
        return this.props.width / this.sizeValue * this.diameter;
    }

    get strokeDashArray() {
        return ProgressCircular.CIRCUMFERENCE;
    }

    get strokeDashOffset() {
        if (this.props.indeterminate !== false) {
            return this.normalizedValue;
        }

        return ((100 - this.normalizedValue) / 100) * ProgressCircular.CIRCUMFERENCE;
    }

    get classes() {
        const classes = {
            'progress-circular': true,
            'progress-circular--visible': true,
            'progress-circular--indeterminate': !!this.props.indeterminate,
            'progress-circular--disable-shrink': this.props.indeterminate === 'disable-shrink',
        }

        if (ProgressCircular.PREDEFINED_SIZES.includes(this.props.size)) {
            classes['progress-circular--size-' + this.props.size] = true;
        }

        classes['progress-circular--' + this.props.color] = true;

        return classes;
    }

    get svgStyles() {
        return stylesToString({
            'transform': `rotate(calc(-90deg + ${Number(this.props.rotate)}deg))`,
        });
    }
}

export const progressCircular = {
    component: ProgressCircular,
    displayName: 'Progress Circular',
    supportedTypes: ['integer'],
    extractProps: ({options}) => ({
        min: options.min,
        max: options.max,
        width: options.width,
        size: options.size,
        rotate: options.rotate,
        color: options.color,
        indeterminate: options.indeterminate,
        hideEmpty: options.hideEmpty,
    }),
};

registry.category('fields').add('progress_circular', progressCircular);
