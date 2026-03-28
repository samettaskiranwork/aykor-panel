// --- 1. ÇEREZDEN İSİM OKUMA ---
function updateUsername() {
    const getCookie = (name) => {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
        return null;
    };
    const rawName = getCookie('user_fullname');
    const navElement = document.getElementById('nav-username');
    if (rawName && navElement) navElement.innerText = decodeURIComponent(rawName);
}

// --- 2. ÇIKIŞ ---
async function handleLogout() {
    if (confirm("Çıkış yapmak istediğinize emin misiniz?")) {
        await fetch('/api/auth/logout');
        window.location.href = '/login';
    }
}

// URL/menü adı ile DOM id bazen farklı (ör. project_list / project-list → section-list)
const SECTION_KEY_BY_PATH = {
    project_list: 'list',
    'project-list': 'list',
    add_project: 'add',
    'add-project': 'add'
};

function isProjectListPath(path) {
    return path === 'list' || path === 'project_list' || path === 'project-list';
}

function isAddProjectPath(path) {
    return path === 'add' || path === 'add_project' || path === 'add-project';
}

// --- 3. NAVİGASYON (ID Korumalı) ---
function navigate(path, updateUrl = true) {
    if (!path) path = 'home';

    document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
    const sectionKey = SECTION_KEY_BY_PATH[path] || path;
    const target = document.getElementById('section-' + sectionKey);

    if (target) {
        target.classList.add('active');
        window.scrollTo(0, 0);
    } else {
        console.warn('navigate: section bulunamadı', path, '→ section-' + sectionKey);
    }

    // DÜZELTME: Eğer path 'edit_project' ise URL'yi burada güncelleme (ID'yi korumak için)
    if (updateUrl && path !== 'edit_project') {
        history.pushState({ section: path }, "", "/" + path);
    }

    try {
        if (path === 'home' && typeof initHomeModule === 'function') initHomeModule();
        if (isProjectListPath(path) && typeof initProjectListModule === 'function') {
            initProjectListModule();
        }
        if (isAddProjectPath(path) && typeof initAddProjectModule === 'function') {
            initAddProjectModule();
        }
        if (path === 'supplier_list' && typeof initSupplierListModule === 'function') initSupplierListModule();
        if (path === 'add_supplier' && typeof initAddSupplierModule === 'function') initAddSupplierModule();

        // Edit sayfası açıldığında yükleme fonksiyonunu tetikle
        if (path === 'edit_project' && typeof initEditProject === 'function') initEditProject();

    } catch (err) {
        console.warn("Modül yükleme hatası:", err);
    }
}

// --- 4. DÜZENLEME SAYFASINI AÇMA (YENİ MANTIK) ---
function openEditPage(type, id) {
    if (!id) return;

    // URL'yi /edit_project/ID şeklinde ayarla
    const targetSection = 'edit_project';
    window.history.pushState({ section: targetSection, id: id }, '', `/${targetSection}/${id}`);

    // Sayfayı aç ama URL'yi bozma (false parametresi önemli)
    navigate(targetSection, false);
}

// --- 5. TARİH VE SAAT (GLOBAL) ---
function updateGlobalStatus() {
    const now = new Date();
    const dateOptions = { day: 'numeric', month: 'long', year: 'numeric', weekday: 'long' };
    const dateEl = document.getElementById('current-date-display');
    if (dateEl) dateEl.innerText = now.toLocaleDateString('tr-TR', dateOptions);

    const timeOptions = { hour: '2-digit', minute: '2-digit', hour12: false };
    // Sadece üst durum çubuğu; home içindeki clock-* şeridi HomeModule tarafından güncellenir
    const clocks = {
        'g-clock-tr': 'Europe/Istanbul', 'g-clock-ny': 'America/New_York',
        'g-clock-de': 'Europe/Berlin', 'g-clock-kr': 'Asia/Seoul', 'g-clock-sg': 'Asia/Singapore'
    };
    for (const [id, tz] of Object.entries(clocks)) {
        const el = document.getElementById(id);
        if (el) el.innerText = now.toLocaleTimeString('tr-TR', { ...timeOptions, timeZone: tz });
    }
}

window.onpopstate = (e) => navigate(e.state ? e.state.section : 'home', false);

window.onload = () => {
    console.log("🚀 Sistem Başlatıldı. Mevcut Adres:", window.location.pathname);

    updateUsername();
    updateGlobalStatus();
    setInterval(updateGlobalStatus, 60000);

    const pathParts = window.location.pathname.split('/');
    const mainPath = pathParts[1] || 'home';

    console.log("📂 Algılanan Sayfa:", mainPath);

    if (mainPath === 'edit_project') {
        console.log("🛠 Edit Sayfası Moduna Giriliyor...");
        navigate('edit_project', false);
    } else {
        navigate(mainPath, false);
    }

};
window.addEventListener('keydown', (e) => {
    // Alt + Z tuşuna basınca geliştirici modunu aç/kapat
    if (e.altKey && e.key.toLowerCase() === 'z') {
        document.body.classList.toggle('debug-mode');

        // Konsola da durum bilgisini basalım ki çalıştığını bilelim
        const isDebug = document.body.classList.contains('debug-mode');
        console.log(isDebug ? "🛠 Geliştirici Modu: AKTİF" : "🛠 Geliştirici Modu: KAPALI");
    }
});