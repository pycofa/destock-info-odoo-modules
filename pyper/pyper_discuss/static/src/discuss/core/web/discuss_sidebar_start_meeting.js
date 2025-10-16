/** @odoo-module */

import {patch} from '@web/core/utils/patch';
import {DiscussSidebarStartMeeting} from '@mail/discuss/call/web/discuss_sidebar_start_meeting';
import {useState} from '@odoo/owl';
import {useService} from '@web/core/utils/hooks';

patch(DiscussSidebarStartMeeting.prototype, {
    setup() {
        super.setup();
        this.threadService = useState(useService('mail.thread'));
    }
});
