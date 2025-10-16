/** @odoo-module **/

import {menuService} from '@web/webclient/menus/menu_service';

const originalStart = menuService.start;

menuService.start = async function (env) {
    const resStart = await originalStart(env);

    env.services.bus_service.subscribe('user_menu_view_changed', async (e) => {
        await resStart.reload();
    });

    return resStart;
};
