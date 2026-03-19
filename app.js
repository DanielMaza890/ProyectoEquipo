// Función para cargar y mostrar las carpetas al abrir la página
async function loadFolders() {
    const response = await fetch('/api/folders');
    const folders = await response.json();
    const grid = document.getElementById('folder-grid');
    grid.innerHTML = ''; 

    folders.forEach(name => {
        const card = document.createElement('div');
        card.className = 'folder-card';
        card.innerHTML = `
            <div class="folder-icon">📁</div>
            <p>${name}</p>
            <div class="actions">
                <button class="edit" onclick="renameFolder('${name}')">✏️</button>
                <button class="delete" onclick="deleteFolder('${name}')">🗑️</button>
            </div>
        `;
        grid.appendChild(card);
    });
}

// Función para CREAR
async function createFolder() {
    const name = prompt("Nombre de la nueva carpeta:");
    if (!name) return;
    const response = await fetch('/api/folders', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name })
    });
    if (response.ok) loadFolders();
}

// Función para RENOMBRAR (Editar)
async function renameFolder(oldName) {
    const newName = prompt("Nuevo nombre:", oldName);
    if (!newName || newName === oldName) return;
    const response = await fetch(`/api/folders/${oldName}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ newName })
    });
    if (response.ok) loadFolders();
}

// Función para ELIMINAR
async function deleteFolder(name) {
    if (confirm(`¿Eliminar "${name}"?`)) {
        const response = await fetch(`/api/folders/${name}`, { method: 'DELETE' });
        if (response.ok) loadFolders();
    }
}

window.onload = loadFolders;