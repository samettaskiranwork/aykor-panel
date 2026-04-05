// static/common/js/utils.js

const TagManager = {
    // Hafızada tutulacak veriler
    engineerMapping: {}, 

    // Sistemi başlatır
    init: function(selectId, containerId, onUpdate) {
        const selectEl = document.getElementById(selectId);
        const containerEl = document.getElementById(containerId);
        let selectedShortNames = [];

        if (!selectEl || !containerEl) return null;

        // Seçim yapıldığında çalışan olay
        selectEl.addEventListener('change', (e) => {
            const shortName = e.target.value;
            const fullName = this.engineerMapping[shortName];

            if (shortName && !selectedShortNames.includes(shortName)) {
                selectedShortNames.push(shortName);
                this.renderTags(containerEl, selectedShortNames, (removedShort) => {
                    selectedShortNames = selectedShortNames.filter(s => s !== removedShort);
                    if (onUpdate) onUpdate(selectedShortNames);
                });
                
                if (onUpdate) onUpdate(selectedShortNames);
            }
            e.target.value = ""; // Dropdown'ı sıfırla
        });

        // Dışarıdan manuel yükleme yapmak için (Edit sayfası için)
        return {
            setValues: (shortNames) => {
                selectedShortNames = shortNames;
                this.renderTags(containerEl, selectedShortNames, (removedShort) => {
                    selectedShortNames = selectedShortNames.filter(s => s !== removedShort);
                    if (onUpdate) onUpdate(selectedShortNames);
                });
            }
        };
    },

    // Etiketleri ekrana basan yardımcı fonksiyon
    renderTags: function(container, list, onRemove) {
        container.innerHTML = '';
        list.forEach(short => {
            const full = this.engineerMapping[short] || short;
            const tag = document.createElement('div');
            tag.className = 'btn-group me-2 mb-2 shadow-sm';
            tag.innerHTML = `
                <span class="btn btn-sm btn-primary disabled" style="opacity: 1;">${full}</span>
                <button type="button" class="btn btn-sm btn-primary" onclick="this.parentElement.dataset.remove='${short}'">
                    <i class="bi bi-x"></i>
                </button>
            `;
            
            // Silme butonu için olay
            tag.querySelector('button').onclick = () => onRemove(short);
            container.appendChild(tag);
        });
    }
};