# Signup Email Verification - French UX

## Description

This module extends `sh_signup_email_approval` to provide French user experience improvements for the email signup verification process, specifically designed for non-technical general public users.

## Features

- ✅ **Pedagogical French messages** - Clear, friendly language for non-technical users
- ✅ **Explanatory text** - Users understand what will happen before clicking buttons
- ✅ **Improved button flow** - "S'inscrire" button that transforms into validation after OTP sent
- ✅ **Better error messages** - Context-aware, helpful French error messages
- ✅ **Visual feedback** - Loading states, color-coded input validation

## Why This Module?

### The Problem with Direct Modification

Modifying the vendor module `sh_signup_email_approval` directly would cause:
- ❌ Loss of changes when module updates
- ❌ Difficulty maintaining and tracking customizations
- ❌ No version control for modifications
- ❌ Unable to toggle features on/off

### The Inheritance Solution

This module uses **Odoo's inheritance pattern** to:
- ✅ Preserve vendor module integrity
- ✅ Survive vendor module updates
- ✅ Enable/disable independently
- ✅ Clear separation of concerns
- ✅ Can be shared or contributed back

## Technical Implementation

### Controller Override
```python
class SignupFrenchUX(otp_auth_AuthSignupHome):
    def auth_send_otp(self, email, **kwargs):
        response = super().auth_send_otp(email, **kwargs)
        # Override success message with pedagogical French text
        return response
```

### Template Inheritance (XPath)
- Adds explanatory alert box before buttons
- Updates labels and placeholders to French
- Hides original signup button
- Renames "Send OTP" to "S'inscrire"

### JavaScript Widget Extension
```javascript
publicWidget.registry.SignUpForm.include({
    _onSendOtp: async function () {
        // French translations via _t()
        // Improved error handling
        // Better UX flow
    }
});
```

## Installation

1. Place module in `addons/` directory
2. Update module list: `odoo-bin -u base -d your_database`
3. Install via Apps menu: Search "Signup Email Verification - French UX"
4. Module automatically depends on `sh_signup_email_approval`

## Dependencies

- `sh_signup_email_approval` (Softhealer Technologies)

## Usage

Once installed, French users will automatically see:

1. **Initial state**: Form with "S'inscrire" button and explanatory text
2. **After click**: Loading state "Envoi en cours..."
3. **After OTP sent**: Alert with pedagogical message, OTP input appears
4. **OTP validation**: Real-time validation with visual feedback
5. **Success**: Form submission with "Inscription en cours..."

## Maintenance

### Updating Vendor Module

When `sh_signup_email_approval` updates:
1. Update the vendor module normally
2. This module continues to work via inheritance
3. Test to ensure compatibility
4. Adjust overrides only if vendor changes affected methods

### Adding More Languages

Copy `i18n/fr.po` and translate to other languages following Odoo conventions.

## License

LGPL-3

## Author

Destock Info
https://destock.info

## Support

For issues specific to French UX, contact: [your-email]
For vendor module issues, contact: support@softhealer.com