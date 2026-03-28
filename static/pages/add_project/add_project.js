 // --- FORMU TEMİZLEME (Yeni kayıt için) ---
    function resetProjectForm() {
        const form = document.getElementById('projectAddForm');
        if (form) form.reset();
        const idField = document.getElementById('projectId');
        if (idField) idField.value = '';

        document.getElementById('add-project-title').innerText = "Add Project";
        document.getElementById('projectSubmitBtn').innerText = "Save Project";

        const codeInput = document.getElementById('input_project_code');
        if (codeInput) {
            codeInput.readOnly = false;
            codeInput.style.backgroundColor = 'white';
        }
    }

    // --- DROPDOWNLARI YÜKLE ---
    async function initAddProjectModule() {
        try {
            const res = await fetch('/api/add-project/dropdowns');
            if (!res.ok) return;
            const d = await res.json();

            const groupSelect = document.getElementById('groupSelect');
            const customerSelect = document.getElementById('customerSelect');
            const engineerSelect = document.getElementById('engineerSelect');

            if (groupSelect) groupSelect.innerHTML = d.groups.map(g => `<option value="${g}">${g}</option>`).join('');
            if (customerSelect) customerSelect.innerHTML = d.customers.map(c => `<option value="${c}">${c}</option>`).join('');
            if (engineerSelect) {
                engineerSelect.innerHTML = d.engineers.map(e =>
                    `<option value="${e.short_name}">${e.full_name} (${e.short_name})</option>`
                ).join('');
            }
        } catch (err) {
            console.error("Dropdown yükleme hatası:", err);
        }
    }

    // --- KAYDET / GÜNCELLE İŞLEMİ ---
    const projectForm = document.getElementById('projectAddForm');
    if (projectForm) {
        projectForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = Object.fromEntries(new FormData(e.target));

            // ID kontrolü: Form içindeki gizli projectId inputundan alıyoruz
            const pid = document.getElementById('projectId').value;
            const url = pid ? `/api/projects/update/${pid}` : '/api/add-project/save';

            const res = await fetch(url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });

            if (res.ok) {
                alert(pid ? "Project Updated Successfully!" : "Project Added Successfully!");
                resetProjectForm();
                navigate('list');
            } else {
                alert("Error saving project!");
            }
        });
    }

    // --- DÜZENLEME MODUNU BAŞLATAN ASIL FONKSİYON ---
    window.setupEditMode = async function (type, id) {
        // 1. Gelen ID'yi kontrol et (undefined ise hemen durdur)
        if (!id || id === 'undefined' || isNaN(id)) {
            console.error("KRİTİK HATA: Fonksiyona gelen ID geçersiz!", id);
            return;
        }

        console.log("Sistem " + id + " ID'li projeyi yüklemeye başlıyor...");

        // 2. Sayfa geçişi
        if (typeof navigate === 'function') navigate('add');

        // 3. Formun ve DOM'un hazır olması için kısa bekleme
        setTimeout(async () => {
            try {
                await initAddProjectModule(); // Dropdownlar gelsin

                const res = await fetch(`/api/projects/get/${id}`);
                if (!res.ok) throw new Error("Veritabanından veri çekilemedi. Durum: " + res.status);

                const p = await res.json();
                console.log("Gelen Veri:", p);

                const form = document.getElementById('projectAddForm');
                if (form) {
                    // Gizli ID inputunu doldur (En önemlisi!)
                    const idField = document.getElementById('projectId');
                    if (idField) idField.value = id;

                    // Form elemanlarını doldur
                    const f = form.elements;
                    if (f['project_code']) f['project_code'].value = p.project_code || '';
                    if (f['customer']) f['customer'].value = p.customer || '';
                    if (f['subject']) f['subject'].value = p.subject || '';
                    if (f['priority']) f['priority'].value = p.priority || 1;
                    if (f['item_quantity']) f['item_quantity'].value = p.item_quantity || 0;
                    if (f['deadline']) f['deadline'].value = p.deadline || '';
                    if (f['proengineer']) f['proengineer'].value = p.proengineer || '';

                    // Görsel başlık
                    document.getElementById('add-project-title').innerText = "Edit Project: " + (p.project_code || '');
                    document.getElementById('projectSubmitBtn').innerText = "Update Project";
                }
            } catch (err) {
                console.error("Yükleme Hatası:", err);
                alert("Proje detayları getirilemedi: " + err.message);
            }
        }, 250); // Bekleme süresini 250ms yaptık
    };


    // İlk açılışta dropdownları yükle
    initAddProjectModule();