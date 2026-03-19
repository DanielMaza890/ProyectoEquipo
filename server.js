const express = require('express');
const fs = require('fs');
const path = require('path');
const multer = require('multer');
const app = express();

const DRIVE_PATH = path.join(__dirname, 'mi_unidad');
if (!fs.existsSync(DRIVE_PATH)) fs.mkdirSync(DRIVE_PATH);

app.use(express.json());
app.use(express.static('.'));

// Configuración de Multer para subir archivos
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        const folderPath = req.query.path || ''; 
        const dest = path.join(DRIVE_PATH, folderPath);
        if (!fs.existsSync(dest)) fs.mkdirSync(dest, { recursive: true });
        cb(null, dest);
    },
    filename: (req, file, cb) => {
        cb(null, file.originalname);
    }
});
const upload = multer({ storage });

// RUTA: Listar carpetas y archivos
app.get('/api/content', (req, res) => {
    const folderPath = req.query.path || '';
    const targetPath = path.join(DRIVE_PATH, folderPath);
    if (!fs.existsSync(targetPath)) return res.status(404).json({error: "No existe"});

    const items = fs.readdirSync(targetPath, { withFileTypes: true });
    const content = items.map(item => ({
        name: item.name,
        isDirectory: item.isDirectory()
    }));
    res.json(content);
});

// RUTA: Crear carpeta
app.post('/api/folders', (req, res) => {
    const { name, path: parentPath } = req.body;
    const newFolderPath = path.join(DRIVE_PATH, parentPath || '', name);
    if (!fs.existsSync(newFolderPath)) fs.mkdirSync(newFolderPath, { recursive: true });
    res.json({ message: 'Carpeta creada' });
});

// RUTA: Subir archivo
app.post('/api/upload', upload.single('file'), (req, res) => {
    res.json({ message: 'Archivo subido' });
});

app.listen(3000, () => console.log('🚀 Drive corriendo en http://localhost:3000'));