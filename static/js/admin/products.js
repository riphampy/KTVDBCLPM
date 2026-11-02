import { apiRequest } from '/js/api.js';
import { showToast, showLoading } from '/js/ui.js';
import { renderNav } from '/js/nav.js';

renderNav();

async function loadProducts() {
    const res = await apiRequest('/admin/products');
    const tbody = document.getElementById('products-list');
    tbody.innerHTML = '';
    res.items.forEach(p => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${p.sku}</td><td>${p.name}</td><td>${p.price}</td><td>${p.stock}</td>
            <td>
                <button data-testid="admin-product-edit-${p.sku}">Sửa</button>
                <button data-testid="admin-product-delete-${p.sku}">Xóa</button>
            </td>
        `;
        tbody.appendChild(tr);
        tr.querySelector(`[data-testid="admin-product-delete-${p.sku}"]`).onclick = () => deleteProduct(p.id);
    });
}

async function deleteProduct(id) {
    if(!confirm('Xóa?')) return;
    try { await apiRequest(`/admin/products/${id}`, { method: 'DELETE' }); loadProducts(); }
    catch(e) { showToast(e.error?.message); }
}

document.getElementById('add-product-btn').onclick = () => document.getElementById('product-form').style.display = 'block';
window.deleteProduct = deleteProduct;

loadProducts();
