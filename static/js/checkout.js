import { apiRequest } from './api.js';
import { showToast } from './ui.js';

document.getElementById('checkout-form').onsubmit = async (e) => {
    e.preventDefault();
    const data = {
        full_name: document.getElementById('full_name').value,
        phone: document.getElementById('phone').value,
        address: document.getElementById('address').value
    };
    try {
        const res = await apiRequest('/orders', { method: 'POST', body: JSON.stringify(data) });
        showToast('Đặt hàng thành công!');
        window.location.href = `/order-detail.html?id=${res.id}`;
    } catch(err) { showToast(err.error?.message || 'Lỗi đặt hàng'); }
};
