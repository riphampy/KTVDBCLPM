import { apiRequest } from './api.js';
import { showToast } from './ui.js';

async function loadOrders() {
    try {
        const res = await apiRequest('/orders');
        const list = document.getElementById('orders-list');
        list.innerHTML = '';
        res.items.forEach(o => {
            const tr = document.createElement('tr');
            tr.setAttribute('data-testid', `order-row-${o.id}`);
            tr.innerHTML = `
                <td><a href="/order-detail.html?id=${o.id}">#${o.id}</a></td>
                <td>${new Date(o.created_at).toLocaleDateString()}</td>
                <td>${o.total_price.toLocaleString('vi-VN')}</td>
                <td data-testid="order-status-${o.id}">${o.status}</td>
                <td>${o.status === 'Chờ xác nhận' ? `<button data-testid="order-cancel-button-${o.id}">Hủy</button>` : ''}</td>
            `;
            if(o.status === 'Chờ xác nhận') tr.querySelector('button').onclick = () => cancelOrder(o.id);
            list.appendChild(tr);
        });
    } catch(e) { showToast(e.error?.message); }
}

async function cancelOrder(id) {
    try { await apiRequest(`/orders/${id}/cancel`, { method: 'POST' }); loadOrders(); }
    catch(e) { showToast(e.error?.message); }
}

loadOrders();
