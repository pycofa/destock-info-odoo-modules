/** @odoo-module */

import {patch} from '@web/core/utils/patch';
import {ListRenderer} from '@web/views/list/list_renderer';

patch(ListRenderer.prototype, {
    getRowClass(record) {
        const classes = super.getRowClass(record).split(' ');
        const selectedIndex = classes.indexOf('table-info');

        if (-1 !== selectedIndex) {
          classes.splice(selectedIndex, 1);
          classes.push('table-primary');
        }

        return classes.join(' ');
    },
});
