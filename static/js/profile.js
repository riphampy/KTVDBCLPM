import { apiRequest } from './api.js';
import { showToast } from './ui.js';

async function loadProfile() {
    const user = await apiRequest('/me');
    document.getElementById('full_name').value = user.full_name;
    document.getElementById('phone').value = user.phone;
}

document.getElementById('profile-form').onsubmit = async (e) => {
    e.preventDefault();
    await apiRequest('/me', { method: 'PUT', body: JSON.stringify({
        full_name: document.getElementById('full_name').value,
        phone: document.getElementById('phone').value
    })});
    showToast('Cập nhật thành công');
};

document.getElementById('password-form').onsubmit = async (e) => {
    e.preventDefault();
    await apiRequest('/me/password', { method: 'PUT', body: JSON.stringify({
        old_password: document.getElementById('old_password').value,
        new_password: document.getElementById('new_password').value,
        confirm_password: document.getElementById('confirm_password').value
    })});
    showToast('Đổi mật khẩu thành công');
};

loadProfile();
