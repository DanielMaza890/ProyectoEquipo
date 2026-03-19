let currentPath = ""; // Para saber en qué carpeta estamos parados

async function loadContent() {
    // Pedimos al servidor el contenido de la carpeta actual
    const response = await fetch(`/api/content?path=${encodeURIComponent(currentPath)}`);
    const items = await response.json();
    
    const grid = document.getElementById('folder-grid');
    grid.innerHTML = ''; // Limpiamos la pantalla
    
    // Actualizamos el texto que dice dónde estamos
    document.getElementById('current-path-display').innerText = `Ubicación: /${currentPath}`;

    items.forEach(item => {
        const card = document.createElement('div');
        card.className = item.isDirectory ? 'folder-card' : 'file-card';
        
        // Ponemos un icono diferente si es carpeta o archivo
        card.innerHTML = `
            <div style="font-size: 50px">${item.isDirectory ? '📁' : '📄'}</div>
            <p>${item.name}</p>
        `;

        // Si es carpeta, al darle clic entramos
        if (item.isDirectory) {
            card.onclick = () => enterFolder(item.name);
        }
        grid.appendChild(card);
    });

    // Función para CREAR CARPETA (Corregida)
async function createFolder() {
    const name = prompt("Nombre de la nueva carpeta:");
    if (!name) return;

    await fetch('/api/folders', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, path: currentPath }) // Enviamos la ruta actual
    });
    loadContent();
}

// Función para ELIMINAR
async function deleteItem(name) {
    if (!confirm(`¿Seguro que quieres borrar "${name}"?`)) return;

    await fetch(`/api/delete?name=${encodeURIComponent(name)}&path=${encodeURIComponent(currentPath)}`, {
        method: 'DELETE'
    });
    loadContent();
}

// Función para EDITAR
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

// Actualiza el dibujo de las tarjetas en loadContent:
// (Dentro del items.forEach, agrega esto a la card)
card.innerHTML += `
    <div class="card-actions">
        <button onclick="renameItem('${item.name}')">✏️</button>
        <button onclick="deleteItem('${item.name}')">🗑️</button>
    </div>
`;
}

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

async function uploadFile() {
    const fileInput = document.getElementById('fileInput');
    if (!fileInput.files[0]) return;

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    // Enviamos el archivo a la ruta actual
    await fetch(`/api/upload?path=${encodeURIComponent(currentPath)}`, {
        method: 'POST',
        body: formData
    });
    
    fileInput.value = ""; // Limpiamos el botón
    loadContent(); // Recargamos para ver el archivo nuevo
}


// Cargar todo al abrir la página
window.onload = loadContent;