import { apiRequest } from '/js/api.js';
import { renderNav } from '/js/nav.js';
renderNav();

document.getElementById('save-stock-btn').onclick = async () => {
    const item = document.querySelector('.item');
    const data = {
        note: document.getElementById('note').value,
        items: [{
            product_id: parseInt(item.querySelector('.pid').value),
            quantity: parseInt(item.querySelector('.qty').value),
            import_price: parseInt(item.querySelector('.price').value)
        }]
    };
    try { await apiRequest('/admin/stock-receipts', { method: 'POST', body: JSON.stringify(data) }); alert('Nhập kho thành công'); }
    catch(e) { alert(e.error?.message); }
};
