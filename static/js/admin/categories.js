import { apiRequest } from '/js/api.js';
import { renderNav } from '/js/nav.js';

renderNav();

async function loadCats() {
    const cats = await apiRequest('/categories');
    const list = document.getElementById('cat-list');
    list.innerHTML = '';
    cats.forEach(c => {
        const li = document.createElement('li');
        li.innerHTML = `${c.name} <button onclick="deleteCat(${c.id})">Xóa</button>`;
        list.appendChild(li);
    });
}

document.getElementById('add-cat-btn').onclick = async () => {
    await apiRequest('/admin/categories', { method: 'POST', body: JSON.stringify({ name: document.getElementById('cat-name').value }) });
    loadCats();
};

window.deleteCat = async (id) => {
    await apiRequest(`/admin/categories/${id}`, { method: 'DELETE' });
    loadCats();
};
loadCats();
