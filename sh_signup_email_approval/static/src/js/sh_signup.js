/* @odoo-module */
import { jsonrpc } from "@web/core/network/rpc_service";
import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.SignUpForm = publicWidget.Widget.extend({
    selector: '#signup_form',
    events: {
        'click #send_otp_btn': '_onSendOtp',
        'input #otp_input': '_onOtpInput',
        'click #signup_btn': '_onsignup'
    },

    init() {
        this._super(...arguments);
        this.rpc = this.bindService("rpc");
    },

    _onSendOtp: async function () {
        const email = document.querySelector('input[name="login"]').value;
        if (!email) {
            alert('Please enter your email.');
            return;
        }

        document.getElementById('otp_section').style.display = 'block';
        document.getElementById('signup_btn').disabled = true;

        const response = await this.rpc('/auth/send_otp', { email });

        if (response.status != 'success') {
            alert(response.message);
        }
    },

    _onOtpInput: async function () {
        const otpInput = document.getElementById('otp_input');
        const signupBtn = document.getElementById('signup_btn');

        otpInput.addEventListener('keyup', async function () {
            const otpValue = otpInput.value;
            signupBtn.disabled = true;
            const email = document.querySelector('input[id="login"]').value;
            const response = await jsonrpc('/auth/verify_otp', { email: email, otp: otpValue });

            if (response.success) {
                signupBtn.disabled = false;
            } else {
                signupBtn.disabled = true;
            }
        });
    },

    _onsignup: async function (event) {
        event.preventDefault();
        const otpValue = $('#otp_input').val();
        const email = $('input[name="login"]').val();
        const signupBtn = $('#signup_btn');

        try {
            // Perform OTP verification using await to handle async call
            const response = await jsonrpc('/auth/verify_otp', { email: email, otp: otpValue });

            if (response.success) {
                signupBtn.prop('disabled', false);
                $('#signup_form')[0].submit();
            } else {
                $('#otp_section').show();
                $('#otp_error').show();
                signupBtn.prop('disabled', true);
            }
        } catch (error) {
            console.error("OTP verification failed:", error);
            alert("An error occurred while verifying the OTP. Please try again.");
        }
    }
});