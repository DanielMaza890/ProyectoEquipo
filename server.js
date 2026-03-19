const express = require('express');
const fs = require('fs');
const path = require('path');
const app = express();
const PORT = 3000;

// Carpeta donde se guardarán los archivos del "Drive"
const DRIVE_PATH = path.join(__dirname, 'mi_unidad');

// Crear la carpeta base si no existe
if (!fs.existsSync(DRIVE_PATH)) {
    fs.mkdirSync(DRIVE_PATH);
}

app.use(express.json());
app.use(express.static('.')); // Sirve el index.html y style.css automáticamente

// RUTA: Listar carpetas (Para que Jazmín las pinte)
app.get('/api/folders', (req, res) => {
    const folders = fs.readdirSync(DRIVE_PATH);
    res.json(folders);
});

// RUTA: Crear carpeta (POST)
app.post('/api/folders', (req, res) => {
    const { name } = req.body;
    const newPath = path.join(DRIVE_PATH, name);
    
    if (!fs.existsSync(newPath)) {
        fs.mkdirSync(newPath);
        return res.status(201).json({ message: 'Carpeta creada con éxito' });
    }
    res.status(400).json({ message: 'La carpeta ya existe' });
});

// RUTA: Eliminar carpeta (DELETE)
app.delete('/api/folders/:name', (req, res) => {
    const folderPath = path.join(DRIVE_PATH, req.params.name);
    if (fs.existsSync(folderPath)) {
        fs.rmSync(folderPath, { recursive: true, force: true });
        return res.json({ message: 'Carpeta eliminada' });
    }
    res.status(404).json({ message: 'No se encontró la carpeta' });
});

app.listen(PORT, () => {
    console.log(`🚀 Servidor corriendo en http://localhost:${PORT}`);
    console.log(`📂 Archivos guardados en: ${DRIVE_PATH}`);
});

// 1. Función para cargar y mostrar las carpetas al abrir la página
async function loadFolders() {
    const response = await fetch('/api/folders');
    const folders = await response.json();
    const grid = document.getElementById('folder-grid');
    grid.innerHTML = ''; // Limpiar antes de recargar

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

// 2. Función para CREAR una carpeta nueva
async function createFolder() {
    const name = prompt("Nombre de la nueva carpeta:");
    if (!name) return;

    const response = await fetch('/api/folders', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name })
    });

    if (response.ok) {
        loadFolders(); // Recargar la lista
    } else {
        alert("Error: La carpeta ya existe o el nombre es inválido.");
    }
}

// 3. Función para ELIMINAR
async function deleteFolder(name) {
    if (confirm(`¿Estás seguro de eliminar "${name}"?`)) {
        const response = await fetch(`/api/folders/${name}`, { method: 'DELETE' });
        if (response.ok) loadFolders();
    }
}

// Ejecutar al cargar la página
window.onload = loadFolders;