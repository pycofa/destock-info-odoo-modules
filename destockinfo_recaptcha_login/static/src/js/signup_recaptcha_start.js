/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

// Only run on /web/signup page
if (window.location.pathname.includes('/web/signup')) {
    console.log('[Destock reCAPTCHA] 🚀 Module signup_recaptcha_start.js loaded on signup page');

    /**
     * Manually start the SignupCaptcha widget on page load
     *
     * This is necessary because /web/signup is not a website page,
     * so publicWidget.registry widgets don't start automatically.
     */
    const startSignupCaptcha = () => {
        console.log('[Destock reCAPTCHA] 🔄 Attempting to start SignupCaptcha widget...');
        const form = document.querySelector('.oe_signup_form');

        if (form && publicWidget.registry.SignupCaptcha) {
            console.log('[Destock reCAPTCHA] ✅ Signup form found, attaching SignupCaptcha widget...');
            const widget = new publicWidget.registry.SignupCaptcha();
            widget.attachTo(form)
                .then(() => {
                    console.log('[Destock reCAPTCHA] ✅ Widget successfully attached to signup form');
                })
                .catch((error) => {
                    console.error('[Destock reCAPTCHA] ❌ Failed to attach widget:', error);
                });
        } else {
            if (!form) {
                console.warn('[Destock reCAPTCHA] ⚠️ Signup form not found on this page');
            }
            if (!publicWidget.registry.SignupCaptcha) {
                console.error('[Destock reCAPTCHA] ❌ SignupCaptcha widget not registered');
            }
        }
    };

    // Try to start immediately if DOM is already loaded
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', startSignupCaptcha);
    } else {
        startSignupCaptcha();
    }
}
