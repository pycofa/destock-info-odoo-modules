/** @odoo-module */

import {WebClient} from '@web/webclient/webclient';
import {patch} from '@web/core/utils/patch';

patch(WebClient.prototype, {
    get defaultTitle() {
        return 'Destock Info';
    },
});
