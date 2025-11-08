/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

/**
 * Manually start the LoginCaptcha widget on page load
 *
 * This is necessary because /web/login is not a website page,
 * so publicWidget.registry widgets don't start automatically.
 */
document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('.oe_login_form');

    if (form && publicWidget.registry.LoginCaptcha) {
        const widget = new publicWidget.registry.LoginCaptcha();
        widget.attachTo(form).catch((error) => {
            console.error('[LoginCaptcha] Failed to attach widget:', error);
        });
    }
});
