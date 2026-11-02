import { apiRequest } from './api.js';
document.querySelector('[data-testid="register-submit-button"]').onclick = async () => {
    const data = {
        email: document.querySelector('[data-testid="register-email-input"]').value,
        password: document.querySelector('[data-testid="register-password-input"]').value,
        confirm_password: document.querySelector('[data-testid="register-confirm-password-input"]').value,
        full_name: document.querySelector('[data-testid="register-full-name-input"]').value,
        phone: document.querySelector('[data-testid="register-phone-input"]').value
    };
    await apiRequest('/auth/register', { method: 'POST', body: JSON.stringify(data) });
    window.location.href = '/login.html';
};