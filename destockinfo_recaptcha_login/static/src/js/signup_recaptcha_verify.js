/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

// Only run on /web/signup page
if (window.location.pathname.includes('/web/signup')) {
    console.log('[Destock reCAPTCHA] 🚀 Verifying reCAPTCHA on signup page...');

    let retryCount = 0;
    const maxRetries = 10; // 10 attempts = 5 seconds max

    const verifySignupCaptcha = () => {
        // Check if SignupCaptcha widget is registered
        if (publicWidget.registry.SignupCaptcha) {
            console.log('[Destock reCAPTCHA] ✅ SignupCaptcha widget is registered (native Odoo module)');

            // Check if reCAPTCHA badge is present
            const badge = document.querySelector('.grecaptcha-badge');
            if (badge) {
                console.log('[Destock reCAPTCHA] ✅ reCAPTCHA badge found (invisible v3)');
            } else {
                console.warn('[Destock reCAPTCHA] ⚠️ reCAPTCHA badge not found yet');
            }

            // Check if signup form is present
            const form = document.querySelector('.oe_signup_form');
            if (form) {
                console.log('[Destock reCAPTCHA] ✅ Signup form found');

                // Add listener to verify token is added on submit
                form.addEventListener('submit', () => {
                    setTimeout(() => {
                        const token = document.querySelector('input[name="recaptcha_token_response"]');
                        if (token && token.value) {
                            console.log('[Destock reCAPTCHA] ✅ reCAPTCHA token added to form');
                        } else {
                            console.warn('[Destock reCAPTCHA] ⚠️ reCAPTCHA token not found in form');
                        }
                    }, 100);
                }, { once: true });
            } else {
                console.warn('[Destock reCAPTCHA] ⚠️ Signup form not found on this page');
            }
        } else {
            retryCount++;
            if (retryCount < maxRetries) {
                // Retry after 500ms
                setTimeout(verifySignupCaptcha, 500);
            } else {
                console.error('[Destock reCAPTCHA] ❌ SignupCaptcha widget NOT registered after ' + maxRetries + ' attempts');
                console.error('[Destock reCAPTCHA] ❌ Check that google_recaptcha module is installed and reCAPTCHA keys are configured');
            }
        }
    };

    // Wait for DOM and widgets to be ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            setTimeout(verifySignupCaptcha, 500);
        });
    } else {
        setTimeout(verifySignupCaptcha, 500);
    }
}
