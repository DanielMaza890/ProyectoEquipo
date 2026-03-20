let currentPath = ""; // Para saber en qué carpeta estamos parados

// 1. Cargar el contenido al iniciar
window.onload = loadContent;

async function loadContent() {
    // Pedimos al servidor el contenido de la carpeta actual
    const response = await fetch(`/api/content?path=${encodeURIComponent(currentPath)}`);
    const items = await response.json();
    
    const grid = document.getElementById('folder-grid');
    if (!grid) return; // Seguridad por si el ID no existe
    grid.innerHTML = ''; // Limpiamos la pantalla
    
    // Actualizamos el texto que dice dónde estamos
    const display = document.getElementById('current-path-display');
    if (display) display.innerText = `Ubicación: /${currentPath}`;

    items.forEach(item => {
        const card = document.createElement('div');
        card.className = item.isDirectory ? 'folder-card' : 'file-card';
        
        // Ponemos el icono, el nombre y los botones de acción
        card.innerHTML = `
            <div style="font-size: 50px" class="icon-click">${item.isDirectory ? '📁' : '📄'}</div>
            <p>${item.name}</p>
            <div class="card-actions">
                <button onclick="event.stopPropagation(); renameItem('${item.name}')">✏️</button>
                <button onclick="event.stopPropagation(); deleteItem('${item.name}')">🗑️</button>
            </div>
        `;

        // Si es carpeta, al darle clic al icono o tarjeta entramos
        if (item.isDirectory) {
            card.onclick = () => enterFolder(item.name);
        }
        
        grid.appendChild(card);
    });
}

// 2. Funciones de Navegación
function enterFolder(folderName) {
    currentPath = currentPath === "" ? folderName : `${currentPath}/${folderName}`;
    loadContent();
}

function goBack() {
    if (currentPath === "") return;
    const parts = currentPath.split('/');
    parts.pop();
    currentPath = parts.join('/');
    loadContent();
}

// 3. Función para SUBIR ARCHIVO
async function uploadFile() {
    const fileInput = document.getElementById('fileInput');
    if (!fileInput || !fileInput.files[0]) return alert("Selecciona un archivo");

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    await fetch(`/api/upload?path=${encodeURIComponent(currentPath)}`, {
        method: 'POST',
        body: formData
    });
    
    fileInput.value = ""; 
    loadContent(); 
}

// 4. Función para CREAR CARPETA
async function createFolder() {
    const name = prompt("Nombre de la nueva carpeta:");
    if (!name) return;

    await fetch('/api/folders', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, path: currentPath })
    });
    loadContent();
}

// 5. Función para ELIMINAR
async function deleteItem(name) {
    if (!confirm(`¿Seguro que quieres borrar "${name}"?`)) return;

    await fetch(`/api/delete?name=${encodeURIComponent(name)}&path=${encodeURIComponent(currentPath)}`, {
        method: 'DELETE'
    });
    loadContent();
}

// 6. Función para RENUMBRAR (Editar)
async function renameItem(oldName) {
    const newName = prompt("Nuevo nombre:", oldName);
    if (!newName || newName === oldName) return;

    await fetch('/api/rename', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ oldName, newName, path: currentPath })
    });
    loadContent();
}
// Cargar todo al abrir la página
window.onload = loadContent;