/** @odoo-module */

import {WebClient} from '@web/webclient/webclient';
import {patch} from '@web/core/utils/patch';
import {onWillStart} from '@odoo/owl';
import {useService} from '@web/core/utils/hooks';

patch(WebClient.prototype, {
    setup() {
        super.setup();
        this.pyperSetupService = useService('pyper_setup');
        this.title.setParts({zopenerp: this.pyperSetupService.appName});

        onWillStart(async () => {
            this.title.setParts({zopenerp: this.pyperSetupService.appName});
        });
    },
});
