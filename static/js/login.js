import { login } from './auth.js';
document.querySelector('[data-testid="login-submit-button"]').onclick = async () => {
    const email = document.querySelector('[data-testid="login-email-input"]').value;
    const password = document.querySelector('[data-testid="login-password-input"]').value;
    await login(email, password);
};