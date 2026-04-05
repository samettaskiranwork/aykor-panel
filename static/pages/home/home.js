/**
 * HOME MODULE - Radikal Temizlik & İstatistik Onarımı
 */
{ // <-- En başa bunu koy
const HomeModule = {
    state: {
        cachedProjects: [],
        currentSort: { key: 'priority', asc: true },
        columnFilters: {},
        targetFriday: null
    },

    // 1. CONFIG: JS tarafında görsel hiçbir şart (bold, badge vb.) kalmadı.
    tableConfig: [
        { label: 'Project Code', key: 'project_code', width: '120px' },
        { label: 'Priority', key: 'priority', center: true, width: '80px' },
        { label: 'Customer', key: 'customer', width: '180px' },
        { label: 'Subject', key: 'subject', width: '250px' },
        { label: 'Item Qty', key: 'item_quantity', center: true, width: '80px' },
        { label: 'Deadline', key: 'deadline', type: 'date', width: '100px' },
        { label: 'Deadline Time', key: 'deadline_time', type: 'time', width: '100px' },
        { label: 'PE', key: 'proengineer', width: '90px' },
        { label: 'Status', key: 'prostatus', center: true, width: '100px' },
        { label: 'Anno Date', key: 'annodate', type: 'date', width: '100px' },
        { label: 'Tender Ref', key: 'tender_reference', width: '130px' }
    ],

    // 2. UTILS: Eksik olan kısım burasıydı, ekledik!
    utils: {
        getTargetFriday() {
            const d = new Date();
            const day = d.getDay();
            let daysToAdd = (day === 6) ? 6 : (day === 0) ? 5 : (5 - day);
            const target = new Date(d);
            target.setDate(d.getDate() + daysToAdd);
            target.setHours(23, 59, 59, 999);
            return target;
        },
        formatTime(seconds) {
            if (!seconds || isNaN(seconds)) return '-';
            const hrs = Math.floor(seconds / 3600);
            const mins = Math.floor((seconds % 3600) / 60);
            return `${hrs.toString().padStart(2, '0')}:${mins.toString().padStart(2, '0')}`;
        }
    },

    ui: {
        renderHeaders() {
            const headers = ['offeredTableHeader', 'mainTableHeader'];
            headers.forEach(id => {
                const thead = document.getElementById(id);
                if (!thead) return;

                thead.innerHTML = `<tr>${HomeModule.tableConfig.map(col => {
                    const isSorted = HomeModule.state.currentSort.key === col.key;
                    const icon = isSorted ? (HomeModule.state.currentSort.asc ? 'bi-sort-down' : 'bi-sort-up') : 'bi-arrow-down-up opacity-25';
                    
                    return `
                    <th style="width: ${col.width}; position: relative;" class="${col.center ? 'text-center' : ''}">
                        <div onclick="HomeModule.logic.sortData('${col.key}')" style="cursor:pointer; white-space:nowrap;">
                            ${col.label} <i class="bi ${icon} ms-1"></i>
                        </div>
                        <input type="text" class="column-filter" placeholder="Ara..." 
                               onkeyup="HomeModule.logic.handleFilter('${col.key}', this.value)">
                    </th>`;
                }).join('')}</tr>`;
            });
        },

        renderRows(targetId, data) {
            const tbody = document.getElementById(targetId);
            if (!tbody) return;

            tbody.innerHTML = data.map(p => {
                const actualId = p.id || p.ID || p.project_id;

                const cells = HomeModule.tableConfig.map(col => {
                    let val = p[col.key] ?? '-';
                    if (col.type === 'date' && val !== '-' && val.includes('-')) {
                        val = val.split('-').reverse().join('.');
                    }
                    if (col.type === 'time' && val !== '-') {
                        val = HomeModule.utils.formatTime(val);
                    }
                    // Status için badge (daire) kodunu sildik, dümdüz metin basıyor.
                    return `<td class="${col.center ? 'text-center' : ''}">${val}</td>`;
                }).join('');

                return `<tr onclick="openEditPage('project', ${actualId})" style="cursor:pointer;">${cells}</tr>`;
            }).join('');
        }
    },

    logic: {
        async init() {
            try {
                // Utils'ten cuma gününü hesapla
                HomeModule.state.targetFriday = HomeModule.utils.getTargetFriday();

                const res = await fetch('/api/home/dashboard_data');
                const data = await res.json();
                
                HomeModule.state.cachedProjects = data.all_projects || data.upcoming_projects || [];
                
                // --- İSTATİSTİK KARTLARINI GÜNCELLEME (Hata Kontrollü) ---
                const stats = data.stats || { working: 0, budget: 0, future: 0 };
                
                const updateEl = (id, val) => {
                    const el = document.getElementById(id);
                    if (el) el.innerText = val || 0;
                };

                updateEl('stat-working', stats.working);
                updateEl('stat-budget', stats.budget);
                updateEl('stat-future', stats.future);

                HomeModule.ui.renderHeaders();
                HomeModule.logic.handleFilter(); 
            } catch (err) { 
                console.error("Home Init Hatası (Büyük ihtimalle Utils eksikliği):", err); 
            }
        },

        handleFilter(key, value) {
            if (key) HomeModule.state.columnFilters[key] = value.toLowerCase();
            const filtered = HomeModule.state.cachedProjects.filter(p => {
                return Object.keys(HomeModule.state.columnFilters).every(fKey => {
                    if (!HomeModule.state.columnFilters[fKey]) return true;
                    return String(p[fKey] || '').toLowerCase().includes(HomeModule.state.columnFilters[fKey]);
                });
            });
            HomeModule.ui.renderRows('mainTableBody', filtered);
            HomeModule.ui.renderRows('offeredTableBody', filtered.filter(p => p.deadline && new Date(p.deadline) <= HomeModule.state.targetFriday));
        },

        sortData(key) {
            const s = HomeModule.state;
            if (s.currentSort.key === key) s.currentSort.asc = !s.currentSort.asc;
            else { s.currentSort.key = key; s.currentSort.asc = true; }
            s.cachedProjects.sort((a, b) => {
                let vA = a[key] ?? ''; let vB = b[key] ?? '';
                return s.currentSort.asc ? String(vA).localeCompare(String(vB), undefined, {numeric: true}) : String(vB).localeCompare(String(vA), undefined, {numeric: true});
            });
            HomeModule.ui.renderHeaders();
            HomeModule.logic.handleFilter();
        }
    }
};

function initHomeModule() { HomeModule.logic.init(); }
}