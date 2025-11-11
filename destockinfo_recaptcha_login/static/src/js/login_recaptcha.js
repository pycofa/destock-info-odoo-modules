/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { ReCaptcha } from "@google_recaptcha/js/recaptcha";

/**
 * Login form reCAPTCHA integration
 *
 * This widget extends the native google_recaptcha module to add support
 * for the login form (/web/login).
 *
 * How it works:
 * 1. On form submit, intercept the event
 * 2. Get a reCAPTCHA token from Google
 * 3. Inject the token as a hidden field
 * 4. Submit the form
 */
publicWidget.registry.LoginCaptcha = publicWidget.Widget.extend({
    selector: ".oe_login_form",
    events: {
        submit: "_onSubmit",
    },

    /**
     * Initialize the reCAPTCHA instance
     */
    init() {
        this._super(...arguments);
        this._recaptcha = new ReCaptcha();
        console.log('[Destock reCAPTCHA] LoginCaptcha widget initialized');
    },

    /**
     * Load Google reCAPTCHA libraries before the widget starts
     */
    async willStart() {
        console.log('[Destock reCAPTCHA] Loading Google reCAPTCHA libraries...');
        const result = await this._recaptcha.loadLibs();
        console.log('[Destock reCAPTCHA] Google reCAPTCHA libraries loaded successfully');
        return result;
    },

    /**
     * Handle form submission with reCAPTCHA validation
     *
     * @param {Event} ev - Submit event
     */
    _onSubmit(ev) {
        // Only add reCAPTCHA if:
        // 1. A public key is configured
        // 2. Token hasn't been added yet
        if (this._recaptcha._publicKey && !this.$el.find("input[name='recaptcha_token_response']").length) {
            console.log('[Destock reCAPTCHA] Form submission intercepted, requesting reCAPTCHA token...');
            ev.preventDefault();

            // Get token from Google with action name "login"
            this._recaptcha.getToken("login").then((tokenCaptcha) => {
                console.log('[Destock reCAPTCHA] Token received successfully, submitting form');
                // Inject token as hidden field
                this.$el.append(
                    `<input name="recaptcha_token_response" type="hidden" value="${tokenCaptcha.token}"/>`,
                );
                // Submit the form
                this.$el.submit();
            });
        } else {
            console.log('[Destock reCAPTCHA] Token already present or no public key, form submitted normally');
        }
    },
});
