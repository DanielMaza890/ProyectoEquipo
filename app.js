async function createFolder() {
    const folderName = prompt("Nombre de la carpeta:");
    if (!folderName) return;

    const response = await fetch('/folder', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ name: folderName })
    });

    if (response.ok) {
        location.reload(); // Refrescar para ver la nueva card
    }
}

async function deleteFolder(name) {
    if (confirm(`¿Borrar ${name}?`)) {
        await fetch(`/folder/${name}`, { method: 'DELETE' });
        location.reload();
    }
}