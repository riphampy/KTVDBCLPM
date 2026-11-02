import { apiRequest } from './api.js';
import { showToast, showLoading } from './ui.js';

let currentPage = 1;

async function loadCategories() {
    try {
        const categories = await apiRequest('/categories');
        const select = document.querySelector('[data-testid="product-category-filter"]');
        categories.forEach(cat => {
            const opt = document.createElement('option');
            opt.value = cat.id;
            opt.textContent = cat.name;
            select.appendChild(opt);
        });
    } catch (err) {
        console.error(err);
    }
}

async function loadProducts(page = 1) {
    currentPage = page;
    showLoading(true);
    const q = document.querySelector('[data-testid="product-search-input"]').value.trim();
    const catId = document.querySelector('[data-testid="product-category-filter"]').value;
    const minPrice = document.querySelector('[data-testid="product-min-price-input"]').value;
    const maxPrice = document.querySelector('[data-testid="product-max-price-input"]').value;
    const sort = document.querySelector('[data-testid="product-sort-select"]').value;

    let url = `/products?page=${page}&size=12`;
    if (q) url += `&q=${encodeURIComponent(q)}`;
    if (catId) url += `&category_id=${catId}`;
    if (minPrice) url += `&min_price=${minPrice}`;
    if (maxPrice) url += `&max_price=${maxPrice}`;
    if (sort) url += `&sort=${sort}`;

    try {
        const res = await apiRequest(url);
        renderProducts(res.items);
        renderPagination(res.page, res.total, res.size);
    } catch (err) {
        showToast(err.error?.message || 'Lỗi tải danh sách sản phẩm');
    } finally {
        showLoading(false);
    }
}

function renderProducts(products) {
    const list = document.getElementById('product-list');
    const empty = document.getElementById('empty-message');
    list.innerHTML = '';

    if (!products || products.length === 0) {
        empty.style.display = 'block';
        return;
    }
    empty.style.display = 'none';

    products.forEach(p => {
        const card = document.createElement('div');
        card.setAttribute('data-testid', `product-card-${p.sku}`);
        card.style.border = '1px solid #ccc';
        card.style.padding = '15px';
        card.style.borderRadius = '4px';

        card.innerHTML = `
            <h3 data-testid="product-card-name-${p.sku}">
                <a href="/product.html?id=${p.id}">${p.name}</a>
            </h3>
            <p>SKU: ${p.sku}</p>
            <p data-testid="product-card-price-${p.sku}">Giá: ${p.price.toLocaleString('vi-VN')} VNĐ</p>
            <p>Tồn kho: ${p.stock}</p>
            <button data-testid="product-add-to-cart-${p.sku}">Thêm vào giỏ</button>
        `;

        card.querySelector(`[data-testid="product-add-to-cart-${p.sku}"]`).onclick = async () => {
            try {
                await apiRequest('/cart/items', {
                    method: 'POST',
                    body: JSON.stringify({ product_id: p.id, quantity: 1 })
                });
                showToast('Đã thêm sản phẩm vào giỏ hàng');
            } catch (err) {
                showToast(err.error?.message || 'Lỗi thêm vào giỏ hàng');
            }
        };

        list.appendChild(card);
    });
}

function renderPagination(page, total, size) {
    const totalPages = Math.ceil(total / size);
    const container = document.getElementById('pagination');
    container.innerHTML = '';

    if (totalPages <= 1) return;

    if (page > 1) {
        const prev = document.createElement('button');
        prev.setAttribute('data-testid', 'pagination-prev');
        prev.textContent = 'Trước';
        prev.onclick = () => loadProducts(page - 1);
        container.appendChild(prev);
    }

    for (let i = 1; i <= totalPages; i++) {
        const pBtn = document.createElement('button');
        pBtn.setAttribute('data-testid', `pagination-page-${i}`);
        pBtn.textContent = i;
        if (i === page) pBtn.style.fontWeight = 'bold';
        pBtn.onclick = () => loadProducts(i);
        container.appendChild(pBtn);
    }

    if (page < totalPages) {
        const next = document.createElement('button');
        next.setAttribute('data-testid', 'pagination-next');
        next.textContent = 'Sau';
        next.onclick = () => loadProducts(page + 1);
        container.appendChild(next);
    }
}

document.querySelector('[data-testid="product-search-button"]').onclick = () => loadProducts(1);
document.querySelector('[data-testid="product-category-filter"]').onchange = () => loadProducts(1);
document.querySelector('[data-testid="product-sort-select"]').onchange = () => loadProducts(1);

loadCategories();
loadProducts(1);
