import { apiRequest } from './api.js';
import { showToast, showLoading } from './ui.js';

const urlParams = new URLSearchParams(window.location.search);
const productId = urlParams.get('id');

if (!productId) {
    window.location.href = '/index.html';
}

async function loadProductDetail() {
    showLoading(true);
    try {
        const product = await apiRequest(`/products/${productId}`);
        document.getElementById('product-name').textContent = product.name;
        document.getElementById('product-sku').textContent = `SKU: ${product.sku}`;
        document.getElementById('product-price').textContent = `Giá: ${product.price.toLocaleString('vi-VN')} VNĐ`;
        document.getElementById('product-stock').textContent = `Tồn kho: ${product.stock}`;
        document.getElementById('product-rating').textContent = `Đánh giá trung bình: ${product.average_rating} / 5 (${product.review_count} lượt)`;

        document.getElementById('add-to-cart-btn').onclick = async () => {
            const qty = parseInt(document.getElementById('product-quantity').value) || 1;
            try {
                await apiRequest('/cart/items', {
                    method: 'POST',
                    body: JSON.stringify({ product_id: product.id, quantity: qty })
                });
                showToast('Đã thêm sản phẩm vào giỏ hàng');
            } catch (err) {
                showToast(err.error?.message || 'Lỗi thêm vào giỏ hàng');
            }
        };
    } catch (err) {
        showToast(err.error?.message || 'Không tìm thấy sản phẩm');
    } finally {
        showLoading(false);
    }
}

async function loadReviews() {
    try {
        const res = await apiRequest(`/products/${productId}/reviews`);
        const list = document.getElementById('reviews-list');
        list.innerHTML = '';

        if (!res.items || res.items.length === 0) {
            list.innerHTML = '<p>Chưa có đánh giá nào cho sản phẩm này.</p>';
            return;
        }

        res.items.forEach(rev => {
            const item = document.createElement('div');
            item.style.borderBottom = '1px solid #eee';
            item.style.padding = '10px 0';
            item.innerHTML = `
                <strong>${rev.user_name || 'Khách hàng'}</strong> - ${rev.rating} sao
                <p>${rev.comment || 'Không có bình luận'}</p>
                <small>${new Date(rev.created_at).toLocaleDateString('vi-VN')}</small>
            `;
            list.appendChild(item);
        });
    } catch (err) {
        console.error(err);
    }
}

document.getElementById('submit-review-btn').onclick = async () => {
    const rating = parseInt(document.getElementById('review-rating').value);
    const comment = document.getElementById('review-comment').value.trim();

    try {
        await apiRequest(`/products/${productId}/reviews`, {
            method: 'POST',
            body: JSON.stringify({ rating, comment })
        });
        showToast('Gửi đánh giá thành công');
        document.getElementById('review-comment').value = '';
        loadProductDetail();
        loadReviews();
    } catch (err) {
        showToast(err.error?.message || 'Lỗi gửi đánh giá');
    }
};

loadProductDetail();
loadReviews();
