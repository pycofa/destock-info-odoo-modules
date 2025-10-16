/** @odoo-module **/

import {
    useRef,
    useEffect,
} from '@odoo/owl';
import {patch} from '@web/core/utils/patch';
import {ControlPanel} from '@web/search/control_panel/control_panel';


patch(ControlPanel.prototype, {
    mainButtonsEnd: undefined,

    setup() {
        super.setup();

        this.mainButtonsEnd = useRef('mainButtonsEnd');

        useEffect(() => {
            // on small screen, clean-up the dropdown elements
            const dropdownButtons = this.mainButtonsEnd.el.querySelectorAll(
                '.o_control_panel_collapsed_create.dropdown-menu button'
            );

            if (!dropdownButtons.length) {
                this.mainButtonsEnd.el
                    .querySelectorAll(
                        '.o_control_panel_collapsed_create.dropdown-menu, .o_control_panel_collapsed_create.dropdown-toggle'
                    )
                    .forEach((el) => el.classList.add('d-none'));

                this.mainButtonsEnd.el
                    .querySelectorAll(".o_control_panel_collapsed_create.btn-group")
                    .forEach((el) => el.classList.remove('btn-group'));

                return;
            }

            for (const button of dropdownButtons) {
                for (const cl of Array.from(button.classList)) {
                    button.classList.toggle(cl, !cl.startsWith('btn-'));
                }

                button.classList.add('dropdown-item', 'btn', 'btn-link');
            }
        });
    },
});
