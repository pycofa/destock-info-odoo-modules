/**
 * Example Jest tests for Odoo JavaScript/OWL components
 * Tests run without Odoo server - local-first testing
 *
 * @module destockinfo_website
 * @description Example test suite demonstrating Jest setup
 */

// Import OWL mocks (automatically mocked by jest.config.js)
import { Component, useState, xml } from '@odoo/owl';
import { utils } from '@web/core/utils';

describe('Example JavaScript Tests', () => {
  test('addition works correctly', () => {
    expect(1 + 1).toBe(2);
  });

  test('string manipulation works', () => {
    const slug = 'Hello World'.toLowerCase().replace(/\s+/g, '-');
    expect(slug).toBe('hello-world');
  });

  test('array operations work', () => {
    const numbers = [1, 2, 3, 4, 5];
    const doubled = numbers.map(n => n * 2);
    expect(doubled).toEqual([2, 4, 6, 8, 10]);
  });
});

describe('Password Toggle Logic', () => {
  beforeEach(() => {
    // Setup DOM before each test
    document.body.innerHTML = `
      <input type="password" id="password" />
      <button id="toggle-btn">Toggle</button>
    `;
  });

  afterEach(() => {
    // Cleanup DOM after each test
    document.body.innerHTML = '';
  });

  test('togglePasswordVisibility changes input type', () => {
    const passwordInput = document.getElementById('password');
    const toggleBtn = document.getElementById('toggle-btn');

    // Simulate toggle function
    function togglePasswordVisibility() {
      passwordInput.type = passwordInput.type === 'password' ? 'text' : 'password';
    }

    expect(passwordInput.type).toBe('password');

    toggleBtn.addEventListener('click', togglePasswordVisibility);
    toggleBtn.click();

    expect(passwordInput.type).toBe('text');

    toggleBtn.click();
    expect(passwordInput.type).toBe('password');
  });

  test('password toggle button changes text', () => {
    const passwordInput = document.getElementById('password');
    const toggleBtn = document.getElementById('toggle-btn');

    function togglePasswordVisibility() {
      const isPassword = passwordInput.type === 'password';
      passwordInput.type = isPassword ? 'text' : 'password';
      toggleBtn.textContent = isPassword ? 'Hide' : 'Show';
    }

    toggleBtn.addEventListener('click', togglePasswordVisibility);

    expect(toggleBtn.textContent).toBe('Toggle');

    toggleBtn.click();
    expect(passwordInput.type).toBe('text');
    expect(toggleBtn.textContent).toBe('Hide');

    toggleBtn.click();
    expect(passwordInput.type).toBe('password');
    expect(toggleBtn.textContent).toBe('Show');
  });
});

describe('Price Formatting', () => {
  test('formats price with currency symbol', () => {
    function formatPrice(amount, currency = '€') {
      return `${amount.toFixed(2)} ${currency}`;
    }

    expect(formatPrice(100)).toBe('100.00 €');
    expect(formatPrice(99.99)).toBe('99.99 €');
    expect(formatPrice(1234.5, '$')).toBe('1234.50 $');
  });

  test('formats price with thousand separators', () => {
    function formatPriceWithSeparator(amount, currency = '€') {
      const formatted = amount.toLocaleString('fr-FR', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
      });
      return `${formatted} ${currency}`;
    }

    // Note: toLocaleString uses non-breaking space (U+00A0) as thousand separator
    expect(formatPriceWithSeparator(1234.56)).toContain('234');
    expect(formatPriceWithSeparator(1234.56)).toContain('56');
    expect(formatPriceWithSeparator(999.99)).toBe('999,99 €');
  });
});

describe('Filter Query String Builder', () => {
  test('builds query string from filters', () => {
    function buildQueryString(filters) {
      const params = new URLSearchParams();
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== null && value !== undefined && value !== '') {
          params.append(key, value);
        }
      });
      return params.toString();
    }

    const filters = {
      brand: 'Dell',
      processor: 'Intel Core i5',
      ram: '16',
      price_min: '100',
      price_max: '500',
    };

    const queryString = buildQueryString(filters);
    expect(queryString).toContain('brand=Dell');
    expect(queryString).toContain('processor=Intel+Core+i5');
    expect(queryString).toContain('ram=16');
  });

  test('ignores empty values in query string', () => {
    function buildQueryString(filters) {
      const params = new URLSearchParams();
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== null && value !== undefined && value !== '') {
          params.append(key, value);
        }
      });
      return params.toString();
    }

    const filters = {
      brand: 'Dell',
      processor: '',
      ram: null,
      price_min: undefined,
    };

    const queryString = buildQueryString(filters);
    expect(queryString).toBe('brand=Dell');
  });
});

describe('OWL Component Mocking', () => {
  test('OWL Component can be instantiated', () => {
    class TestComponent extends Component {}

    const component = new TestComponent();
    expect(component).toBeInstanceOf(Component);
    expect(component.env).toBeDefined();
    expect(component.props).toBeDefined();
  });

  test('useState mock works', () => {
    const state = { count: 0 };
    const reactiveState = useState(state);

    expect(useState).toHaveBeenCalledWith(state);
    expect(reactiveState).toEqual(state);
  });

  test('xml template function works', () => {
    const template = xml`<div class="test">Hello World</div>`;
    expect(xml).toHaveBeenCalled();
    expect(typeof template).toBe('string');
  });
});

describe('Odoo Utils Mocking', () => {
  test('debounce mock returns function', () => {
    const mockFn = jest.fn();
    const debouncedFn = utils.debounce(mockFn);

    expect(typeof debouncedFn).toBe('function');
    expect(utils.debounce).toHaveBeenCalledWith(mockFn);
  });

  test('escapeRegExp mock is callable', () => {
    utils.escapeRegExp('test.*');
    expect(utils.escapeRegExp).toHaveBeenCalledWith('test.*');
  });
});

describe('Product Card Toggle Logic', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <div class="product-card" data-product-id="123">
        <button class="btn-wishlist" data-action="add-to-wishlist">
          <i class="fa fa-heart-o"></i>
        </button>
      </div>
    `;
  });

  test('wishlist button toggles icon class', () => {
    const button = document.querySelector('.btn-wishlist');
    const icon = button.querySelector('i');

    function toggleWishlist() {
      icon.classList.toggle('fa-heart-o');
      icon.classList.toggle('fa-heart');
    }

    expect(icon.classList.contains('fa-heart-o')).toBe(true);

    toggleWishlist();
    expect(icon.classList.contains('fa-heart')).toBe(true);
    expect(icon.classList.contains('fa-heart-o')).toBe(false);

    toggleWishlist();
    expect(icon.classList.contains('fa-heart-o')).toBe(true);
    expect(icon.classList.contains('fa-heart')).toBe(false);
  });
});

describe('Form Validation', () => {
  test('validates email format', () => {
    function isValidEmail(email) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return emailRegex.test(email);
    }

    expect(isValidEmail('test@example.com')).toBe(true);
    expect(isValidEmail('user.name+tag@domain.co.uk')).toBe(true);
    expect(isValidEmail('invalid.email')).toBe(false);
    expect(isValidEmail('missing@domain')).toBe(false);
    expect(isValidEmail('@domain.com')).toBe(false);
  });

  test('validates required fields', () => {
    function validateForm(formData) {
      const requiredFields = ['name', 'email', 'phone'];
      const errors = [];

      requiredFields.forEach(field => {
        if (!formData[field] || formData[field].trim() === '') {
          errors.push(`${field} is required`);
        }
      });

      return {
        isValid: errors.length === 0,
        errors,
      };
    }

    const validForm = {
      name: 'John Doe',
      email: 'john@example.com',
      phone: '0123456789',
    };

    const invalidForm = {
      name: '',
      email: 'john@example.com',
      phone: '',
    };

    expect(validateForm(validForm).isValid).toBe(true);
    expect(validateForm(invalidForm).isValid).toBe(false);
    expect(validateForm(invalidForm).errors).toHaveLength(2);
  });
});
