/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

console.log('[Destock reCAPTCHA] 🚀 Module login_recaptcha_start.js loaded');

/**
 * Manually start the LoginCaptcha widget on page load
 *
 * This is necessary because /web/login is not a website page,
 * so publicWidget.registry widgets don't start automatically.
 */
const startLoginCaptcha = () => {
    console.log('[Destock reCAPTCHA] 🔄 Attempting to start LoginCaptcha widget...');
    const form = document.querySelector('.oe_login_form');

    if (form && publicWidget.registry.LoginCaptcha) {
        console.log('[Destock reCAPTCHA] ✅ Login form found, attaching LoginCaptcha widget...');
        const widget = new publicWidget.registry.LoginCaptcha();
        widget.attachTo(form)
            .then(() => {
                console.log('[Destock reCAPTCHA] ✅ Widget successfully attached to login form');
            })
            .catch((error) => {
                console.error('[Destock reCAPTCHA] ❌ Failed to attach widget:', error);
            });
    } else {
        if (!form) {
            console.warn('[Destock reCAPTCHA] ⚠️ Login form not found on this page');
        }
        if (!publicWidget.registry.LoginCaptcha) {
            console.error('[Destock reCAPTCHA] ❌ LoginCaptcha widget not registered');
        }
    }
};

// Try to start immediately if DOM is already loaded
if (document.readyState === 'loading') {
    console.log('[Destock reCAPTCHA] DOM is loading, waiting for DOMContentLoaded...');
    document.addEventListener('DOMContentLoaded', startLoginCaptcha);
} else {
    console.log('[Destock reCAPTCHA] DOM already loaded, starting immediately...');
    startLoginCaptcha();
}
