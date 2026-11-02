import { apiRequest } from '/js/api.js';
import { renderNav } from '/js/nav.js';
renderNav();

document.getElementById('rev-btn').onclick = async () => {
    const from = document.getElementById('from').value;
    const to = document.getElementById('to').value;
    const res = await apiRequest(`/admin/reports/revenue?from=${from}&to=${to}`);
    const table = document.getElementById('report-table');
    table.innerHTML = res.data.map(d => `<tr><td>${d.date || d.period}</td><td>${d.revenue}</td></tr>`).join('');
};
