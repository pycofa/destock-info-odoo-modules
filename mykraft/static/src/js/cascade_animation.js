/** @odoo-module */

import {WebClient} from '@web/webclient/webclient';
import {patch} from '@web/core/utils/patch';
import {useBus} from '@web/core/utils/hooks';

patch(WebClient.prototype, {
    setup() {
        super.setup();
        useBus(this.env.bus, "ACTION_MANAGER:UI-UPDATED", this.animateRouteChanged);
    },

    animateRouteChanged() {
        const parent_kanban = document.querySelector('.o_kanban_group');
        const parent_list = document.querySelector('.o_list_table .ui-sortable');

        if (parent_kanban) {
            const children_kanban = parent_kanban.querySelectorAll('.o_kanban_record');

            children_kanban.forEach((child, index) => {
                child.style.animationDelay = `${index * 0.03}s`;
            });
        }

        if (parent_list) {
            const children_list = parent_list.querySelectorAll('.o_data_row');

            children_list.forEach((child, index) => {
                child.style.animationDelay = `${index * 0.01}s`;
            });
        }
    },
});