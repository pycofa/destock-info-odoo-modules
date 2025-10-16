/** @odoo-module */

import {Dialog} from '@web/core/dialog/dialog';
import {useService} from '@web/core/utils/hooks';
import {patch} from '@web/core/utils/patch';

patch(Dialog.prototype, {
    setup() {
        super.setup();

        this.pyperSetupService = useService('pyper_setup');

        if (Dialog.defaultProps.title === this.props.title && this.pyperSetupService.appName) {
            this.props.title = this.pyperSetupService.appName
        }
    },
});
