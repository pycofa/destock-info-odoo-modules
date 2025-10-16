/** @odoo-module */

import {patch} from '@web/core/utils/patch';
import {ControlPanel} from '@web/search/control_panel/control_panel';
import {ViewsSwitcher} from './views_switcher';


patch(ControlPanel.prototype, {
    get displayViewSwitcherEntries() {
        return this.env.config.viewSwitcherEntries?.length > 1;
    },
});

ControlPanel.components.ViewsSwitcher = ViewsSwitcher;
