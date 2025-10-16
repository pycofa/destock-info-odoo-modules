/** @odoo-module **/

import {_t} from '@web/core/l10n/translation';
import {registry} from '@web/core/registry';

const userMenuItemsCategory = registry.category('user_menuitems');

export function switchDrawerMinifiableItem(env) {
    if (!env.services['drawer'].minifiable) {
        return false;
    }

    return {
        type: 'switch',
        id: 'pyper_drawer.switch_minifiable',
        description: _t('Mini Drawer'),
        callback: () => {
            env.services['drawer'].minified = !env.services['drawer'].minified;
        },
        isChecked: env.services['drawer'].minified,
        sequence: 30,
    };
}

export function switchDrawerLockableItem(env) {
    return {
        type: 'switch',
        id: 'pyper_drawer.switch_lockable',
        description: _t('Lockable Drawer'),
        callback: () => {
            env.services['drawer'].lockable = !env.services['drawer'].lockable;
        },
        isChecked: env.services['drawer'].lockable,
        sequence: 30,
    };
}

userMenuItemsCategory.add('drawer_minifiable.switch', switchDrawerMinifiableItem);
userMenuItemsCategory.add('drawer_lockable.switch', switchDrawerLockableItem);
