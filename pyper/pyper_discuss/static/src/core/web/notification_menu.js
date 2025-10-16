/** @odoo-module */

import {Component, useState} from '@odoo/owl';
import {registry} from '@web/core/registry';
import {useService} from '@web/core/utils/hooks';

export class NotificationMenu extends Component {
    static template = 'pyper_discuss.NotificationMenu';

    static props = [];

    setup() {
        this.store = useState(useService('mail.store'));
        this.threadService = useState(useService('mail.thread'));
        this.actionService = useService('action');
    }

    get counter() {
        return this.store.discuss.inbox.counter;
    }

    onClick() {
        const action = this.counter > 0 ? 'mail.box_inbox' : 'mail.box_history';
        this.actionService.doAction('mail.action_discuss', {additionalContext: {display_mode: 'notifications', action_id: action}});
    }
}

registry
    .category('systray')
    .add('pyper_discuss.notification_menu', {Component: NotificationMenu}, {sequence: 50})
;
