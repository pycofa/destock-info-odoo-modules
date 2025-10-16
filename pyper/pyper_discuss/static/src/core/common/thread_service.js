/** @odoo-module */

import {patch} from '@web/core/utils/patch';
import {ThreadService} from '@mail/core/common/thread_service';

const NOTIFICATION_IDS = [
    'mail.action_discuss',
    'mail.box_inbox',
    'mail.box_starred',
    'mail.box_history',
];

patch(ThreadService.prototype, {
    displayMode: 'channels',

    updateDisplayMode(action) {
        let mode = action.context?.display_mode;

        if (mode) {
            this.displayMode = mode;
            return;
        }

        this.displayMode =  NOTIFICATION_IDS.includes(action?.context?.active_id) || NOTIFICATION_IDS.includes(action?.params?.action)
            ? 'notifications'
            : 'channels';
    }
});
