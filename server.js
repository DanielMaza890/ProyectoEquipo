const express = require('express');
const fs = require('fs');
const path = require('path');
const app = express();
const PORT = 3000;

// Carpeta donde se guardarán las carpetas físicas en tu compu
const DRIVE_PATH = path.join(__dirname, 'mi_unidad');

if (!fs.existsSync(DRIVE_PATH)) {
    fs.mkdirSync(DRIVE_PATH);
}

app.use(express.json());
app.use(express.static('.')); // Esto hace que index.html sea visible

// RUTA: Listar carpetas
app.get('/api/folders', (req, res) => {
    const folders = fs.readdirSync(DRIVE_PATH);
    res.json(folders);
});

// RUTA: Crear carpeta
app.post('/api/folders', (req, res) => {
    const { name } = req.body;
    const newPath = path.join(DRIVE_PATH, name);
    if (!fs.existsSync(newPath)) {
        fs.mkdirSync(newPath);
        return res.status(201).json({ message: 'Carpeta creada' });
    }
    res.status(400).json({ message: 'La carpeta ya existe' });
});

// RUTA: Renombrar carpeta (¡Agrégala para que el botón de editar funcione!)
app.put('/api/folders/:oldName', (req, res) => {
    const { newName } = req.body;
    const oldPath = path.join(DRIVE_PATH, req.params.oldName);
    const newPath = path.join(DRIVE_PATH, newName);
    if (fs.existsSync(oldPath)) {
        fs.renameSync(oldPath, newPath);
        return res.json({ message: 'Carpeta renombrada' });
    }
    res.status(404).send();
});

// RUTA: Eliminar carpeta
app.delete('/api/folders/:name', (req, res) => {
    const folderPath = path.join(DRIVE_PATH, req.params.name);
    if (fs.existsSync(folderPath)) {
        fs.rmSync(folderPath, { recursive: true, force: true });
        return res.json({ message: 'Carpeta eliminada' });
    }
    res.status(404).json({ message: 'No se encontró' });
});

app.listen(PORT, () => {
    console.log(`🚀 Servidor en http://localhost:${PORT}`);
});