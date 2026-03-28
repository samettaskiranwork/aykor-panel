async function initSupplierListModule() {
    const tbody = document.getElementById('supplierTableBody');
    if (!tbody) return;
    try {
        const res = await fetch('/api/suppliers/list');
        if (!res.ok) throw new Error(await res.text());
        const rows = await res.json();
        tbody.innerHTML = (Array.isArray(rows) ? rows : []).map(s => `
            <tr>
                <td>${escapeHtml(s.ncage_code ?? '')}</td>
                <td>${escapeHtml(s.supplier_name ?? '')}</td>
                <td>${escapeHtml(s.country ?? '')}</td>
                <td>${s.website ? `<a href="${escapeAttr(s.website)}" target="_blank" rel="noopener">${escapeHtml(s.website)}</a>` : ''}</td>
            </tr>
        `).join('');
    } catch (e) {
        console.error('Supplier list:', e);
        tbody.innerHTML = '<tr><td colspan="4" class="text-center text-danger">Liste yüklenemedi</td></tr>';
    }
}

function escapeHtml(t) {
    const d = document.createElement('div');
    d.textContent = t;
    return d.innerHTML;
}

function escapeAttr(t) {
    return String(t).replace(/"/g, '&quot;');
}
