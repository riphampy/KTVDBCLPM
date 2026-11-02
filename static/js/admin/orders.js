import { apiRequest } from '/js/api.js';
import { renderNav } from '/js/nav.js';

renderNav();

async function loadOrders() {
    const res = await apiRequest('/admin/orders');
    const tbody = document.getElementById('admin-orders-list');
    tbody.innerHTML = '';
    res.items.forEach(o => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>#${o.id}</td><td>${o.full_name}</td><td>${o.total_price}</td>
            <td>
                <select data-testid="admin-order-status-select-${o.id}">
                    <option value="Chờ xác nhận" ${o.status==='Chờ xác nhận'?'selected':''}>Chờ xác nhận</option>
                    <option value="Đã xác nhận" ${o.status==='Đã xác nhận'?'selected':''}>Đã xác nhận</option>
                    <option value="Đang giao" ${o.status==='Đang giao'?'selected':''}>Đang giao</option>
                    <option value="Hoàn thành" ${o.status==='Hoàn thành'?'selected':''}>Hoàn thành</option>
                    <option value="Đã hủy" ${o.status==='Đã hủy'?'selected':''}>Đã hủy</option>
                </select>
            </td>
            <td><button data-testid="admin-order-status-save-${o.id}">Cập nhật</button></td>
        `;
        tr.querySelector(`[data-testid="admin-order-status-save-${o.id}"]`).onclick = async () => {
            const status = tr.querySelector(`[data-testid="admin-order-status-select-${o.id}"]`).value;
            try {
                await apiRequest(`/admin/orders/${o.id}/status`, { method: 'PATCH', body: JSON.stringify({ status }) });
                alert('Cập nhật thành công');
                loadOrders();
            } catch(e) { alert(e.error?.message || 'Lỗi'); }
        };
        tbody.appendChild(tr);
    });
}
loadOrders();
