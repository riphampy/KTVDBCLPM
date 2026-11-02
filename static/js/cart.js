import { apiRequest } from './api.js';
import { showToast, showLoading } from './ui.js';

async function loadCart() {
    showLoading(true);
    try {
        const cart = await apiRequest('/cart');
        const tbody = document.getElementById('cart-items');
        tbody.innerHTML = '';
        cart.items.forEach(item => {
            const tr = document.createElement('tr');
            tr.setAttribute('data-testid', `cart-row-${item.sku}`);
            tr.innerHTML = `
                <td>${item.name}</td>
                <td>${item.price.toLocaleString('vi-VN')}</td>
                <td><input type="number" data-testid="cart-item-quantity-${item.sku}" value="${item.quantity}" min="1" max="99"></td>
                <td data-testid="cart-item-line-total-${item.sku}">${item.line_total.toLocaleString('vi-VN')}</td>
                <td><button data-testid="cart-item-remove-${item.sku}">Xóa</button></td>
            `;
            tbody.appendChild(tr);
            tr.querySelector('input').onchange = (e) => updateQty(item.product_id, e.target.value);
            tr.querySelector('button').onclick = () => removeItem(item.product_id);
        });
        document.getElementById('subtotal').textContent = cart.subtotal.toLocaleString('vi-VN') + ' VNĐ';
        document.getElementById('shipping-fee').textContent = cart.shipping_fee.toLocaleString('vi-VN') + ' VNĐ';
        document.getElementById('total').textContent = cart.total.toLocaleString('vi-VN') + ' VNĐ';
    } catch(e) { showToast(e.error?.message); }
    finally { showLoading(false); }
}

async function updateQty(pid, qty) {
    try { await apiRequest(`/cart/items/${pid}`, { method: 'PUT', body: JSON.stringify({ quantity: qty }) }); loadCart(); }
    catch(e) { showToast(e.error?.message); loadCart(); }
}

async function removeItem(pid) {
    try { await apiRequest(`/cart/items/${pid}`, { method: 'DELETE' }); loadCart(); }
    catch(e) { showToast(e.error?.message); }
}

document.getElementById('clear-cart').onclick = async () => {
    try { await apiRequest('/cart', { method: 'DELETE' }); loadCart(); }
    catch(e) { showToast(e.error?.message); }
}

loadCart();
