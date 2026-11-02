// nav.js - Logic này sẽ được gọi ở mỗi trang để render thanh điều hướng
export function renderNav() {
    const user = JSON.parse(localStorage.getItem('user'));
    const nav = document.getElementById('main-nav');
    // Render HTML dựa trên role và cập nhật cart count từ API
}
