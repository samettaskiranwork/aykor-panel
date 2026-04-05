async function initEditProject() {
    const form = document.getElementById('editProjectForm');
    if (form) form.reset();

    // --- 1. ID ÇEKME (GARANTİ YÖNTEM) ---
    const pathParts = window.location.pathname.split('/');
    // Boşlukları temizleyip son parçayı alalım (trailing slash koruması)
    const lastPart = pathParts.filter(p => p !== "").pop();

    console.log("🔍 Adres çubuğundan okunan ID:", lastPart);

    if (!lastPart || isNaN(lastPart)) {
        console.warn("⚠️ Geçerli bir ID bulunamadı, işlem durduruldu.");
        return;
    }

    try {
        // --- 2. DROPDOWN DOLDURMA ---
        const dropdownRes = await fetch('/api/projects/get-dropdowns');
        const dropdowns = await dropdownRes.json();

        const customerSelect = document.getElementById('customer');
        if (customerSelect) {
            customerSelect.innerHTML = '<option value="">Seçiniz...</option>' +
                dropdowns.customers.map(c => `<option value="${c}">${c}</option>`).join('');
        }

        const peSelect = document.getElementById('proengineer');
        if (peSelect) {
            peSelect.innerHTML = '<option value="">Seçiniz...</option>' +
                dropdowns.engineers.map(e => `<option value="${e}">${e}</option>`).join('');
        }

        // --- 3. VERİ ÇEKME ---
        console.log(`📡 Python'dan ${lastPart} ID'li proje isteniyor...`);
        const response = await fetch(`/api/edit-projects/get/${lastPart}`);
        const data = await response.json();
        console.log("✅ Gelen veri:", data);
        const finalId = data.id || lastPart;
        // --- 4. FORMU DOLDURMA ---
        // 150ms bekleme süresi dropdownların yerleşmesi için daha güvenlidir
        setTimeout(() => {
            // 1. Önce gelen veriyi kutulara doldur
            Object.keys(data).forEach(key => {
                const element = document.getElementById(key);
                if (element) {
                    element.value = data[key] ?? '';
                }
            });

            // 2. ID'yi mühürle (Eğer data.id null ise, lastPart yani 16'yı kullan)
            const fixedId = data.id || lastPart;
            const form = document.getElementById('editProjectForm');
            if (form) {
                form.dataset.currentId = fixedId;
                console.log("📌 Formun işlem yapacağı ID kesinleşti:", fixedId);
            }
        }, 150);

    } catch (error) {
        console.error("❌ initEditProject Hatası:", error);
    }
}

// Sayfa yüklendiğinde çalıştır (SPA kontrolü dashboard.js'de olsa da buraya da emniyet koyalım)
if (window.location.pathname.includes('edit_project')) {
    initEditProject();
}

// Submit İşlemi
document.getElementById('editProjectForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const projectId = window.location.pathname.split('/').pop();
    const formData = new FormData(e.target);
    const updateData = Object.fromEntries(formData.entries());

    try {
        const response = await fetch(`/api/edit-projects/update/${projectId}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(updateData)
        });

        const result = await response.json();
        if (result.status === "success") {
            alert("Başarıyla güncellendi!");
        } else {
            alert("Hata: " + result.detail);
        }
    } catch (error) {
        alert("Sistem hatası oluştu.");
    }
});

// Sayfaya her girişte çalıştır
initEditProject();