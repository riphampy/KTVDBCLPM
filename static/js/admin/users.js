import { apiRequest } from '/js/api.js';
import { renderNav } from '/js/nav.js';
renderNav();

async function loadUsers() {
    const res = await apiRequest('/admin/users');
    const tbody = document.getElementById('users-list');
    tbody.innerHTML = '';
    res.items.forEach(u => {
        const tr = document.createElement('tr');
        tr.innerHTML = `<td>${u.email}</td><td>${u.full_name}</td><td>${u.locked ? 'Khóa' : 'Hoạt động'}</td>
        <td><button data-testid="admin-user-lock-${u.id}" onclick="toggleLock(${u.id}, ${!u.locked})">${u.locked ? 'Mở' : 'Khóa'}</button></td>`;
        tbody.appendChild(tr);
    });
}
window.toggleLock = async (id, locked) => {
    await apiRequest(`/admin/users/${id}/lock`, { method: 'PATCH', body: JSON.stringify({ locked }) });
    loadUsers();
};
loadUsers();
