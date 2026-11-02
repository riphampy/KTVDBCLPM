import { apiRequest } from './api.js';

export async function login(email, password) {
    const data = await apiRequest('/auth/login', { method: 'POST', body: JSON.stringify({ email, password }) });
    localStorage.setItem('token', data.token);
    localStorage.setItem('user', JSON.stringify(data.user));
    window.location.href = '/index.html';
}

export function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/login.html';
}
