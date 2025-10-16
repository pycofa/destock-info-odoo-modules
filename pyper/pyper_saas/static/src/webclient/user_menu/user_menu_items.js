/** @odoo-module **/

// Import dependency to init the user_menuitems registry
import '@web/webclient/user_menu/user_menu';
import {registry} from '@web/core/registry';

const userRegistry = registry.category('user_menuitems');
userRegistry.remove('documentation');
userRegistry.remove('support');
userRegistry.remove('odoo_account');
