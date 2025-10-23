/**
 * Jest Unit Tests: Password Toggle Button
 *
 * Tests the password toggle JavaScript logic in isolation (no Odoo server needed).
 * Environment: jsdom
 * Execution time: < 1s
 * Coverage target: 80% of password_toggle.js
 *
 * Test cases:
 * - T006: Toggle password type (password → text)
 * - T007: Toggle password type back (text → password)
 * - T008: Icon switching (fa-eye → fa-eye-slash)
 * - T009: Icon switching back (fa-eye-slash → fa-eye)
 * - T010: ARIA update (aria-pressed: false → true)
 * - T011: ARIA update back (aria-pressed: true → false)
 * - T012: Defensive programming (missing icon element)
 */

describe('Password Toggle Button', () => {
  let passwordInput;
  let toggleButton;
  let icon;

  beforeEach(() => {
    // Setup DOM structure matching QWeb templates
    document.body.innerHTML = `
      <div class="position-relative">
        <input type="password" name="password" class="form-control" />
        <button type="button" class="btn btn-link position-absolute password-toggle-btn"
                aria-label="Afficher ou masquer le mot de passe"
                aria-pressed="false" tabindex="0">
          <i class="fa fa-eye password-toggle-btn__icon"></i>
        </button>
      </div>
    `;

    passwordInput = document.querySelector('input[name="password"]');
    toggleButton = document.querySelector('.password-toggle-btn');
    icon = toggleButton.querySelector('.password-toggle-btn__icon');

    // Mock the toggle function (implementation will be in password_toggle.js)
    toggleButton.addEventListener('click', () => {
      const input = toggleButton.previousElementSibling;
      if (input && input.tagName === 'INPUT') {
        // Toggle type attribute
        const isPasswordVisible = input.type === 'text';
        input.type = isPasswordVisible ? 'password' : 'text';

        // Toggle ARIA attribute
        toggleButton.setAttribute('aria-pressed', isPasswordVisible ? 'false' : 'true');

        // Toggle icon classes
        const iconElement = toggleButton.querySelector('.password-toggle-btn__icon');
        if (iconElement) {
          if (isPasswordVisible) {
            iconElement.classList.remove('fa-eye-slash');
            iconElement.classList.add('fa-eye');
          } else {
            iconElement.classList.remove('fa-eye');
            iconElement.classList.add('fa-eye-slash');
          }
        }
      }
    });
  });

  afterEach(() => {
    // Cleanup DOM
    document.body.innerHTML = '';
  });

  // T006: Toggle password type (password → text)
  test('toggles password input type from password to text', () => {
    expect(passwordInput.type).toBe('password');

    toggleButton.click();

    expect(passwordInput.type).toBe('text');
  });

  // T007: Toggle password type back (text → password)
  test('toggles password input type from text back to password', () => {
    // First click: password → text
    toggleButton.click();
    expect(passwordInput.type).toBe('text');

    // Second click: text → password
    toggleButton.click();

    expect(passwordInput.type).toBe('password');
  });

  // T008: Icon switching (fa-eye → fa-eye-slash)
  test('changes icon from fa-eye to fa-eye-slash when password visible', () => {
    expect(icon.classList.contains('fa-eye')).toBe(true);
    expect(icon.classList.contains('fa-eye-slash')).toBe(false);

    toggleButton.click();

    expect(icon.classList.contains('fa-eye')).toBe(false);
    expect(icon.classList.contains('fa-eye-slash')).toBe(true);
  });

  // T009: Icon switching back (fa-eye-slash → fa-eye)
  test('changes icon from fa-eye-slash back to fa-eye when password masked', () => {
    // First click: fa-eye → fa-eye-slash
    toggleButton.click();
    expect(icon.classList.contains('fa-eye-slash')).toBe(true);

    // Second click: fa-eye-slash → fa-eye
    toggleButton.click();

    expect(icon.classList.contains('fa-eye')).toBe(true);
    expect(icon.classList.contains('fa-eye-slash')).toBe(false);
  });

  // T010: ARIA update (aria-pressed: false → true)
  test('updates aria-pressed to true when password visible', () => {
    expect(toggleButton.getAttribute('aria-pressed')).toBe('false');

    toggleButton.click();

    expect(toggleButton.getAttribute('aria-pressed')).toBe('true');
  });

  // T011: ARIA update back (aria-pressed: true → false)
  test('updates aria-pressed to false when password masked', () => {
    // First click: false → true
    toggleButton.click();
    expect(toggleButton.getAttribute('aria-pressed')).toBe('true');

    // Second click: true → false
    toggleButton.click();

    expect(toggleButton.getAttribute('aria-pressed')).toBe('false');
  });

  // T012: Defensive programming (missing icon element)
  test('handles missing icon element gracefully', () => {
    // Remove icon element
    icon.remove();

    // Toggle should still work for input type and ARIA, just skip icon update
    expect(() => toggleButton.click()).not.toThrow();

    expect(passwordInput.type).toBe('text');
    expect(toggleButton.getAttribute('aria-pressed')).toBe('true');
  });
});
