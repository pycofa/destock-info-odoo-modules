/** @odoo-module **/

import {reactive} from '@odoo/owl';
import {registry} from '@web/core/registry';
import {jsonrpc} from '@web/core/network/rpc_service';
import {debounce} from '@web/core/utils/timing';


export class MenuCounterState {
    constructor(bus) {
        this.bus = bus;
    }

    setup() {
        this.state = {
            request: null,
            values: {},
            intervalId: null,
        };

        this.loadCounters = debounce(this.loadCounters.bind(this), this.debounceDelay);
        this.bus.addEventListener('MENUS-COUNTER:LOAD', this.loadCounters);
    }

    get debounceDelay() {
        return 1000;
    }

    get interval() {
        return 60000;
    }

    get loading() {
        return !!this.state.request;
    }

    get values() {
        return this.state.values;
    }

    registerMenuItem(menuItemId) {
        this.state.values[menuItemId] = undefined;

        // Create interval if new menu item is registered and interval is not created before
        if (!this.state.intervalId) {
            this.intervalId = setInterval(() => {
                this.loadCounters().then();
            }, this.interval);
        }

        this.loadCounters().then();
    }

    unregisterMenuItem(menuItemId) {
        delete this.state.values[menuItemId];

        // Clean interval if no menu item is registered
        if (this.state.intervalId && Object.keys(this.state.values).length === 0) {
            if (this.state.request) {
                this.state.request.abort();
            }

            clearInterval(this.state.intervalId);
            this.state.intervalId = null;
        }
    }

    async loadCounters() {
        const ids = Object.keys(this.state.values);

        if (this.loading || !ids.length) {
            return;
        }

        try {
            this.state.request = jsonrpc('/web/webclient/load_menu_counters', {ids});

            const res = await this.state.request;
            this.state.values = mergeValues(this.state.values, res.menuCounters);
            this.bus.trigger('MENUS-COUNTER:LOADED', this.state.values);
        } catch (e) {
            // Skip errors
        } finally {
            this.state.request = null;
        }
    }
}

function mergeValues(obj1, obj2) {
    for (const key of Object.keys(obj1)) {
        if (obj2.hasOwnProperty(key)) {
            obj1[key] = obj2[key];
        } else {
            obj1[key] = 0;
        }
    }

    return obj1;
}

export const drawerService = {
    start(env) {
        const menuCounterState = reactive(new MenuCounterState(env.bus));
        menuCounterState.setup();

        return menuCounterState;
    },
};

registry.category('services').add('menu_counter', drawerService);
