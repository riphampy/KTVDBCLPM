export function showToast(message) {
    const toast = document.getElementById('toast');
    toast.textContent = message; toast.style.display = 'block';
    setTimeout(() => toast.style.display = 'none', 3000);
}

export function showLoading(show) {
    document.getElementById('loading').style.display = show ? 'flex' : 'none';
}
