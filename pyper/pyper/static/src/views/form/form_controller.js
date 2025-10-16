/** @odoo-module */

import {patch} from '@web/core/utils/patch';
import {FormController} from '@web/views/form/form_controller';
import {useBus} from '@web/core/utils/hooks';

patch(FormController.prototype, {
    setup() {
        super.setup();
        useBus(this.model.bus, 'JS_ON_EVENT', this._onJsEvent);
    },

    async _onJsEvent(event) {
        if (typeof this[event.detail] === 'function') {
            this[event.detail]();
        }
    },
});
