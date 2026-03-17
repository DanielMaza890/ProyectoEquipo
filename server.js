const express = require('express');
const fs = require('fs');
const app = express();
app.use(express.json());

const BASE_DIR = './mis_archivos';

// Crear carpeta
app.post('/folder', (req, res) => {
    const { name } = req.body;
    const path = `${BASE_DIR}/${name}`;
    if (!fs.existsSync(path)){
        fs.mkdirSync(path);
        return res.status(201).send({ message: 'Carpeta creada' });
    }
    res.status(400).send({ message: 'Ya existe' });
});

// Eliminar carpeta
app.delete('/folder/:name', (req, res) => {
    const path = `${BASE_DIR}/${req.params.name}`;
    fs.rmSync(path, { recursive: true, force: true });
    res.send({ message: 'Eliminada' });
});

app.listen(3000, () => console.log('Servidor en puerto 3000'));