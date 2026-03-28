/**
 * PROJECT LIST MODULE - Temiz ve Modüler Versiyon
 */
const ProjectListModule = {
    state: {
        fullData: [],
        filters: {},
        currentSort: { key: 'id', asc: false }
    },

    // 1. CONFIG: JS tarafında görsel şartları sildik (Bold ve Badge CSS'e emanet)
    tableConfig: [
        { label: 'Project Code', key: 'project_code', width: '130px' },
        { label: 'Priority', key: 'priority', center: true, width: '80px' },
        { label: 'Customer', key: 'customer', width: '200px' },
        { label: 'Subject', key: 'subject', width: '280px' },
        { label: 'Item Qty', key: 'item_quantity', center: true, width: '80px' },
        { label: 'Deadline', key: 'deadline', type: 'date', width: '110px' },
        { label: 'PE', key: 'proengineer', width: '100px' },
        { label: 'Status', key: 'prostatus', center: true, width: '110px' }
    ],

    ui: {
        // Başlıkları ve Filtre Kutularını Çizer
        renderHeaders() {
            const thead = document.getElementById('projectListHeader');
            if (!thead) return;

            thead.innerHTML = `<tr>${ProjectListModule.tableConfig.map(col => `
                <th style="width: ${col.width}; position: relative;" class="${col.center ? 'text-center' : ''}">
                    <div onclick="ProjectListModule.logic.sort('${col.key}')" style="cursor:pointer;">
                        ${col.label} <i class="bi bi-arrow-down-up opacity-25 ms-1"></i>
                    </div>
                    <input type="text" class="column-filter" placeholder="Ara..." 
                           onkeyup="ProjectListModule.logic.handleFilter('${col.key}', this.value)">
                </th>`).join('')}</tr>`;
        },

        // Satırları Çizer (Sorgusuz & Sualsiz)
        renderRows(data) {
            const tbody = document.getElementById('projectTableBody');
            const countEl = document.getElementById('project-count');
            if (!tbody) return;

            if (countEl) countEl.innerText = `${data.length} Projects`;

            tbody.innerHTML = data.map(p => {
                const realId = p.id || p.ID || p.project_id;
                
                const cells = ProjectListModule.tableConfig.map(col => {
                    let val = p[col.key] ?? '-';
                    // Sadece tarih formatı (görsel değil, yapısal format)
                    if (col.type === 'date' && val !== '-' && val.includes('-')) {
                        val = val.split('-').reverse().join('.');
                    }
                    return `<td class="${col.center ? 'text-center' : ''}">${val}</td>`;
                }).join('');

                return `<tr onclick="openEditPage('project', ${realId})" style="cursor:pointer;">${cells}</tr>`;
            }).join('');
        }
    },

    logic: {
        async init() {
            console.log("📂 Project List verisi çekiliyor...");
            try {
                // Not: API yolunu kontrol et, home_api içindeki veriyi de kullanabilirsin
                const res = await fetch('/api/home/dashboard_data'); 
                const data = await res.json();
                
                // Backend'den 'all_projects' anahtarıyla gelen veriyi alıyoruz
                ProjectListModule.state.fullData = data.all_projects || [];
                
                ProjectListModule.ui.renderHeaders();
                ProjectListModule.logic.handleFilter();
            } catch (err) {
                console.error("❌ Liste yüklenemedi:", err);
            }
        },

        handleFilter(key, value) {
            if (key) ProjectListModule.state.filters[key] = value.toLowerCase();
            
            const filtered = ProjectListModule.state.fullData.filter(p => {
                return Object.keys(ProjectListModule.state.filters).every(fKey => {
                    if (!ProjectListModule.state.filters[fKey]) return true;
                    return String(p[fKey] || '').toLowerCase().includes(ProjectListModule.state.filters[fKey]);
                });
            });
            ProjectListModule.ui.renderRows(filtered);
        },

        sort(key) {
            const s = ProjectListModule.state;
            s.currentSort.asc = s.currentSort.key === key ? !s.currentSort.asc : true;
            s.currentSort.key = key;

            s.fullData.sort((a, b) => {
                let vA = a[key] ?? ''; let vB = b[key] ?? '';
                return s.currentSort.asc 
                    ? String(vA).localeCompare(String(vB), undefined, {numeric: true}) 
                    : String(vB).localeCompare(String(vA), undefined, {numeric: true});
            });
            ProjectListModule.logic.handleFilter();
        }
    }
};

// Modülü uyandırmak için global fonksiyon
function initProjectListModule() {
    ProjectListModule.logic.init();
}