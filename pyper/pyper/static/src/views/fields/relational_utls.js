/** @odoo-module */

import {Many2XAutocomplete} from '@web/views/fields/relational_utils';

export class ImageMany2XAutocomplete extends Many2XAutocomplete {
    mapRecordToOption(result) {
        return {
            ...super.mapRecordToOption(result),
            resModel: this.props.resModel,
        };
    }

    get optionsSource() {
        return {
            ...super.optionsSource,
            optionTemplate: 'pyper.ImageMany2XAutocomplete',
        };
    }
}
