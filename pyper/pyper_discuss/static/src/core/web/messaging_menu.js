/** @odoo-module */

import {MessagingMenu} from '@mail/core/web/messaging_menu';
import {patch} from '@web/core/utils/patch';

patch(MessagingMenu.prototype, {
    getThreads() {
        // Exclude need action notifications
        return super.getThreads().filter(
            (thread) =>
                !(thread.needactionMessages.length > 0 && thread.type === 'chatter')
        );
    },

    get counter() {
        // Remove value of inbox counter
        return super.counter - this.store.discuss.inbox.counter;
    }
});
