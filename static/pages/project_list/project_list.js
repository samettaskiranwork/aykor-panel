// --- PROJECT LIST ÇEKMECESİ ---
let fullProjectData = [];
let projectSort = { key: 'id', asc: false };
let projectFilters = {};

const projectTableConfig = [
    { label: 'Project Code', key: 'project_code', bold: true, width: '130px' },
    { label: 'Priority', key: 'priority', center: true, width: '80px' },
    { label: 'Customer', key: 'customer', width: '200px' },
    { label: 'Subject', key: 'subject', width: '280px' },
    { label: 'Item Qty', key: 'item_quantity', center: true, width: '80px' },
    { label: 'Deadline', key: 'deadline', type: 'date', width: '110px' },
    { label: 'PE', key: 'proengineer', width: '100px' },
    { label: 'Status', key: 'prostatus', center: true, badge: true, width: '110px' }
];

// 1. BAŞLATICI: Sayfa açıldığında sadece veriyi çeker
async function initProjectListModule() {
    try {
        const res = await fetch('/api/projects/'); 
        fullProjectData = await res.json();
        renderProjectHeaders();
        renderProjectRows(fullProjectData);
        
        // Tablo genişletme aletini çalıştır
        if (typeof initProjectResizers === 'function') initProjectResizers();
    } catch (err) {
        console.error("Liste yüklenemedi:", err);
    }
}

// 2. TABLO ÇİZİMİ: Sadece görseli basar
function renderProjectRows(dataToRender) {
    const tbody = document.getElementById('projectTableBody');
    if (!tbody) return;

    document.getElementById('project-count').innerText = `${dataToRender.length} Proje`;

    tbody.innerHTML = dataToRender.map(p => {
        const realId = p.id || p.ID || p.project_id;
        const cells = projectTableConfig.map(col => {
            let val = p[col.key] ?? '-';
            if (col.type === 'date' && val !== '-') val = val.split('-').reverse().join('.');
            if (col.bold) val = `<strong>${val}</strong>`;
            if (col.badge && val !== '-') val = `<span class="badge bg-light text-dark border">${val}</span>`;
            return `<td class="${col.center ? 'text-center' : ''}">${val}</td>`;
        }).join('');

        // Tıklama olayı dashboard.html'deki ANA openEditPage'e gider
        return `<tr onclick="openEditPage('project', ${realId})" style="cursor:pointer;">${cells}</tr>`;
    }).join('');
}

// 3. FİLTRELEME VE SIRALAMA: Akıl kısmı
function handleProjectFilter(key, value) {
    if (key) projectFilters[key] = value.toLowerCase();
    const filtered = fullProjectData.filter(p => {
        return Object.keys(projectFilters).every(fKey => {
            if (!projectFilters[fKey]) return true;
            return String(p[fKey] || '').toLowerCase().includes(projectFilters[fKey]);
        });
    });
    renderProjectRows(filtered);
}

// Sorting ve Header fonksiyonlarını da buraya ekleyebilirsin...