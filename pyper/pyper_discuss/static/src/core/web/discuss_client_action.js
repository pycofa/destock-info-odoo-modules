/** @odoo-module */

import {patch} from '@web/core/utils/patch';
import {DiscussClientAction} from '@mail/core/web/discuss_client_action';

patch(DiscussClientAction.prototype, {
    async restoreDiscussThread(props) {
        // Update display mode in thread service
        this.threadService.updateDisplayMode(props.action);

        // Select the first channel if display mode is 'channels'
        if (this.threadService.displayMode === 'channels' && props.action.params) {
            for (const thread of this.store.menuThreads) {
                if (thread.model === 'discuss.channel' && thread.type === 'channel') {
                    props.action.params['active_id'] = this.store.Thread.localIdToActiveId(thread.localId);
                    break;
                }
            }
        } else if (this.threadService.displayMode === 'notifications') {
            if (props.action?.context?.action_id && !props.action?.context?.active_id) {
                props.action.context.active_id = props.action?.context?.action_id;
            }
        }

        super.restoreDiscussThread(props);
    },
});
