/** @odoo-module */

import {registry} from '@web/core/registry';
import {Many2OneField, many2OneField} from '@web/views/fields/many2one/many2one_field';
import {useSpecialData} from '@web/views/fields/relational_utils';
import {useService} from '@web/core/utils/hooks';

export class Many2OneBadgeField extends Many2OneField {
    static template = 'pyper.Many2OneFieldBadge';

    static props = {
        ...Many2OneField.props,
        colorField: {
            type: String,
            required: false,
        },
        iconField: {
            type: String,
            required: false,
        },
        noIcon: {
            type: Boolean,
        },
    }

    setup() {
        super.setup();
        this.fieldService = useService('field');
        this.colorType = 'integer';

        this.specialData = useSpecialData(async (orm, props) => {
            const {name, record} = props;
            const fieldConfig = record.fields[name];
            const value = record.data[name];

            if (value[0] && value.length < 3) {
                const relFields = await this.fieldService.loadFields(fieldConfig.relation);
                const specification = {};

                if (relFields[props.colorField]) {
                    specification[props.colorField] = {};
                    this.colorType = relFields[props.colorField].type;
                }

                if (relFields[props.iconField]) {
                    specification[props.iconField] = {};
                }

                if (Object.keys(specification).length > 0) {
                    const v= await orm.webRead(fieldConfig.relation, [value[0]], {specification});
                    value.push(v[0][props.colorField] || undefined);
                    value.push(v[0][props.iconField] || undefined);
                } else {
                    value.push(undefined);
                    value.push(undefined);
                }
            }

            return value;
        });
    }

    get badgeStyles() {
        const styles = {
            color: this.colorType !== 'integer' && this.value[2] ? this.value[2] : undefined,
        };

        if (this.colorType !== 'integer') {
            styles['background-color'] = 'color-mix(in srgb, ' + this.value[2] + ' var(--pyper-many2one-badge-bg-opacity), transparent)';
        }

        return Object.entries(styles).map(([k, v]) => `${k}: ${v} !important;`).join('');
    }

    get badgeClasses() {
        let colorClass = 'o_colorlist_badge_color_' + (this.value[2] || 0);

        return {
            [colorClass]: this.colorType === 'integer',
        };
    }

    get iconClasses() {
        return {
            'o_badge_icon': true,
            [this.value[3]]: !!this.value[3],
        };
    }
}

export const many2OneBadgeField = {
    ...many2OneField,
    component: Many2OneBadgeField,
    extractProps(fieldInfo, dynamicInfo) {
        const res = many2OneField.extractProps(fieldInfo, dynamicInfo);
        res['colorField'] = fieldInfo.options['color_field'] || 'color';
        res['iconField'] = fieldInfo.options['icon_field'] || 'icon';
        res['noIcon'] = fieldInfo.options['no_icon'] || false;

        return res;
    },
};

registry.category('fields').add('many2one_badge', many2OneBadgeField);
registry.category('fields').add('list.many2one_badge', many2OneBadgeField);
registry.category('fields').add('kanban.many2one_badge', many2OneBadgeField);
