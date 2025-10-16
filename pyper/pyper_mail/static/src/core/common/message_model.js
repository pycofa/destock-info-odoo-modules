/* @odoo-module */

import {patch} from '@web/core/utils/patch';
import {Message} from '@mail/core/common/message_model';

patch(Message.prototype, {
    get hasTextContent() {
        // Force to display messages related to an email activity type in the chatter without body
        return this['mail_activity_type_name'] ? true : super.hasTextContent;
    },

    get isEmpty() {
        // Force to display messages related to an activity type in the chatter
        return this['mail_activity_type_name'] ? false : super.isEmpty;
    },
});
