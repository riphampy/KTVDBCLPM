const API_BASE = '/api';

export async function apiRequest(endpoint, options = {}) {
    const token = localStorage.getItem('token');
    const headers = { 'Content-Type': 'application/json', ...options.headers };
    if (token) headers['Authorization'] = `Bearer ${token}`;

    const response = await fetch(`${API_BASE}${endpoint}`, { ...options, headers });
    if (response.status === 401) { localStorage.removeItem('token'); window.location.href = '/login.html'; }
    if (response.status === 403) window.location.href = '/403.html';
    
    const data = await response.json();
    if (!response.ok) throw data;
    return data;
}
