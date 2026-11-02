export function renderNav() {
    const user = JSON.parse(localStorage.getItem('user'));
    const nav = document.getElementById('main-nav');
    if (!nav) return;

    let html = '<a href="/index.html">Sản phẩm</a> | ';
    if (user) {
        html += `<a href="/cart.html" data-testid="nav-cart-link">Giỏ hàng (<span data-testid="nav-cart-count" id="cart-count">0</span>)</a> | `;
        html += `<a href="/orders.html">Đơn hàng</a> | <a href="/profile.html">Hồ sơ</a> | `;
        html += `<button data-testid="nav-logout-button" id="logout-btn">Đăng xuất</button> (${user.full_name})`;
        if (user.role === 'admin') html += ' | <a href="/admin/products.html">Admin</a>';
    } else {
        html += '<a href="/login.html" data-testid="nav-login-link">Đăng nhập</a> | <a href="/register.html" data-testid="nav-register-link">Đăng ký</a>';
    }
    nav.innerHTML = html;

    if (document.getElementById('logout-btn')) {
        document.getElementById('logout-btn').onclick = () => { localStorage.clear(); window.location.href = '/login.html'; };
    }
}
renderNav();
