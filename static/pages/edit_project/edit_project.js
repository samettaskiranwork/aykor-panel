// --- 1. GLOBAL DEĞİŞKENLER (Pencere Seviyesinde) ---
if (typeof window.isEditProjectLoading === 'undefined') {
    window.isEditProjectLoading = false;
}
let selectedShortNames = [];
let engineerMapping = {};

const statusMeanings = {
    "10.02": "Tender is under evaluation by NSPA.",
    "10.01": "Tender prepared and submitted.",
    "20.01": "Project won and starting."
};

// --- 2. YARDIMCI FONKSİYONLAR (Dışarıda Olmalı) ---

function renderTags() {
    const container = document.getElementById('selected_pe_tags');
    if (!container) return;

    container.innerHTML = '';
    selectedShortNames.forEach(short => {
        const full = engineerMapping[short] || short;
        const tag = document.createElement('div');
        tag.className = 'btn-group me-2 mb-2 shadow-sm';
        tag.innerHTML = `
            <span class="btn btn-sm btn-primary disabled" style="opacity: 1; font-weight: 500;">${full}</span>
            <button type="button" class="btn btn-sm btn-primary" onclick="removeTag('${short}')">
                <i class="bi bi-x-lg"></i>
            </button>
        `;
        container.appendChild(tag);
    });
}

window.removeTag = function (short) {
    selectedShortNames = selectedShortNames.filter(name => name !== short);
    renderTags();
};

function updateStatusDescription(statusValue) {
    const descBox = document.getElementById('status_description');
    if (descBox) {
        descBox.value = statusMeanings[statusValue] || "Açıklama bulunamadı...";
    }
}

// --- 3. ANA BAŞLATICI (DASHBOARD ÇAĞIRIR) ---
async function initEditProject() {
    if (window.isEditProjectLoading) {
        console.warn("🛑 Dur! Başka bir initEditProject zaten çalışıyor.");
        return;
    }
    window.isEditProjectLoading = true;

    const form = document.getElementById('editProjectForm');
    if (form) form.reset();

    selectedShortNames = [];
    renderTags();

    const pathParts = window.location.pathname.split('/');
    const lastPart = pathParts.filter(p => p !== "").pop();

    if (!lastPart || isNaN(lastPart)) {
        window.isEditProjectLoading = false;
        return;
    }

    try {
        // --- DROPDOWNLARI DOLDUR ---
        const dropdownRes = await fetch('/api/projects/get-dropdowns');
        const dropdowns = await dropdownRes.json();

        const peSelect = document.getElementById('proengineer');
        if (peSelect && dropdowns.engineers) {
            peSelect.innerHTML = '<option value="">Mühendis Seçiniz...</option>';
            dropdowns.engineers.forEach(eng => {
                // eng: { full_name: "Can Türkoğlu", short_name: "CT" } şeklinde geliyor
                engineerMapping[eng.short_name] = eng.full_name;

                const option = document.createElement('option');
                option.value = eng.short_name;

                // DİKKAT: Sadece eng yazarsan [object Object] çıkar. 
                // eng.full_name yazmalısın!
                option.textContent = eng.full_name;

                peSelect.appendChild(option);
            });
        }

        const customerSelect = document.getElementById('customer');
        if (customerSelect) {
            customerSelect.innerHTML = '<option value="">Seçiniz...</option>' +
                dropdowns.customers.map(c => `<option value="${c}">${c}</option>`).join('');
        }

        const statusSelect = document.getElementById('prostatus');
        if (statusSelect) {
            statusSelect.innerHTML = '<option value="">Seçiniz...</option>' +
                Object.keys(statusMeanings).map(s => `<option value="${s}">${s}</option>`).join('');
        }

        // --- VERİ ÇEKME VE DOLDURMA ---
        console.log(`📡 Python'dan ${lastPart} ID'li proje isteniyor...`);
        const response = await fetch(`/api/edit-projects/get/${lastPart}`);
        const data = await response.json();

        setTimeout(() => {
            Object.keys(data).forEach(key => {
                const element = document.getElementById(key);
                if (element) { element.value = data[key] ?? ''; }
            });

            if (data.proengineer) {
                selectedShortNames = data.proengineer.split(',')
                    .map(s => s.trim())
                    .filter(s => s !== "");
                renderTags();
            }

            updateStatusDescription(data.prostatus);

            if (form) {
                form.dataset.currentId = data.id || lastPart;
                console.log("📌 Formun işlem yapacağı ID:", form.dataset.currentId);
            }
        }, 150);

    } catch (error) {
        console.error("❌ Hata:", error);
    } finally {
        setTimeout(() => {
            window.isEditProjectLoading = false;
        }, 500);
    }
}

// --- 4. OLAY DİNLEYİCİLERİ (BİR KEZ TANIMLANIR) ---

// PE Seçimi
document.getElementById('proengineer')?.addEventListener('change', function (e) {
    const shortName = e.target.value;
    if (shortName && !selectedShortNames.includes(shortName)) {
        selectedShortNames.push(shortName);
        renderTags();
    }
    this.value = "";
});

// Statü Değişimi
document.getElementById('prostatus')?.addEventListener('change', (e) => {
    updateStatusDescription(e.target.value);
});

// Kaydetme
document.getElementById('editProjectForm')?.addEventListener('submit', async function (e) {
    e.preventDefault();
    const projectId = this.dataset.currentId || window.location.pathname.split('/').pop();
    const formData = new FormData(this);
    const updateData = Object.fromEntries(formData.entries());
    updateData.proengineer = selectedShortNames.join(', ');

    try {
        const response = await fetch(`/api/edit-projects/update/${projectId}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(updateData)
        });
        const result = await response.json();
        if (result.status === "success") { alert("✅ Başarıyla güncellendi!"); }
        else { alert("❌ Hata: " + result.detail); }
    } catch (error) { alert("Sistem hatası!"); }
});

// !!! ÖNEMLİ !!!
// Dosyanın en altında initEditProject(); gibi bir çağırma VARSA SİL!