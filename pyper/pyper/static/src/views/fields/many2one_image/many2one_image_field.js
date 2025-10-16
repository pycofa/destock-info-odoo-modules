/** @odoo-module **/

import {Component} from '@odoo/owl';
import {_t} from '@web/core/l10n/translation';
import {registry} from '@web/core/registry';
import {usePopover} from '@web/core/popover/popover_hook';
import {many2OneField, Many2OneField} from '@web/views/fields/many2one/many2one_field';

import {ImageMany2XAutocomplete} from '../relational_utls';

export class Many2OneImageField extends Component {
    static template = 'pyper.Many2OneImageField';

    static components = {
        Many2OneField,
    };

    static props = {
        ...Many2OneField.props,
    };

    get relation() {
        return this.props.relation || this.props.record.fields[this.props.name].relation;
    }

    get many2OneProps() {
        return Object.fromEntries(
            Object.entries(this.props).filter(
                ([key, _val]) => key in this.constructor.components.Many2OneField.props
            )
        );
    }
}

export const many2OneImageField = {
    ...many2OneField,
    component: Many2OneImageField,
    extractProps(fieldInfo) {
        const props = many2OneField.extractProps(...arguments);
        props.canOpen = fieldInfo.viewType === 'form';

        return props;
    },
};

export class Many2OneFieldImagePopover extends Many2OneField {
    static props = {
        ...Many2OneField.props,
        close: {
            type: Function,
        },
    };

    static components = {
        Many2XAutocomplete: ImageMany2XAutocomplete,
    };

    get Many2XAutocompleteProps() {
        return {
            ...super.Many2XAutocompleteProps,
            dropdown: false,
            autofocus: true,
        };
    }

    async updateRecord(value) {
        const updatedValue = await super.updateRecord(...arguments);
        await this.props.record.save();

        return updatedValue;
    }
}

export class KanbanMany2OneImageField extends Many2OneImageField {
    static template = 'pyper.KanbanMany2OneImageField';

    static props = {
        ...Many2OneImageField.props,
        isEditable: {
            type: Boolean,
            optional: true,
        },
    };

    setup() {
        super.setup();
        this.popover = usePopover(Many2OneFieldImagePopover, {
            popoverClass: 'o_m2o_tags_image_field_popover',
            closeOnClickAway: (target) => !target.closest('.modal'),
        });
    }

    get popoverProps() {
        const props = {
            ...this.props,
            readonly: false,
        };
        delete props.isEditable;

        return props;
    }

    openPopover(ev) {
        if (!this.props.isEditable) {
            return;
        }

        this.popover.open(ev.currentTarget, {
            ...this.popoverProps,
            canCreate: false,
            canCreateEdit: false,
            canQuickCreate: false,
            placeholder: _t('Search record...'),
        });
    }
}

export const kanbanMany2OneImageField = {
    ...many2OneField,
    component: KanbanMany2OneImageField,
    additionalClasses: ['o_field_many2one_image_kanban'],
    extractProps(fieldInfo, dynamicInfo) {
        const props = many2OneImageField.extractProps(...arguments);
        props.isEditable = !dynamicInfo.readonly;

        return props;
    },
};

registry.category('fields').add('many2one_image', many2OneImageField);
registry.category('fields').add('kanban.many2one_image', kanbanMany2OneImageField);
