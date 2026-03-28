function initAddSupplierModule() {
    const form = document.getElementById('supplierForm');
    if (!form || form.dataset.supplierBound === '1') return;
    form.dataset.supplierBound = '1';
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const fd = new FormData(form);
        const body = {
            supplier_name: fd.get('supplier_name'),
            ncage_code: fd.get('ncage_code') || null,
            country: fd.get('country') || null,
            website: fd.get('website') || null
        };
        try {
            const res = await fetch('/api/suppliers/add', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body)
            });
            if (!res.ok) throw new Error(await res.text());
            form.reset();
            alert('Tedarikçi kaydedildi.');
            if (typeof navigate === 'function') navigate('supplier_list');
        } catch (err) {
            console.error(err);
            alert('Kayıt başarısız.');
        }
    });
}
