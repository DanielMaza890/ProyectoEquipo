let currentPath = "";

async function loadContent() {
    const response = await fetch(`/api/content?path=${currentPath}`);
    const items = await response.json();
    const grid = document.getElementById('folder-grid');
    grid.innerHTML = '';
    
    document.getElementById('current-path-display').innerText = `Ubicación: /${currentPath}`;

    items.forEach(item => {
        const card = document.createElement('div');
        card.className = item.isDirectory ? 'folder-card' : 'file-card';
        card.innerHTML = `
            <div style="font-size: 40px">${item.isDirectory ? '📁' : '📄'}</div>
            <p>${item.name}</p>
        `;
        if (item.isDirectory) {
            card.onclick = () => enterFolder(item.name);
        }
        grid.appendChild(card);
    });
}

function enterFolder(name) {
    currentPath = currentPath === "" ? name : `${currentPath}/${name}`;
    loadContent();
}

function goBack() {
    const parts = currentPath.split('/');
    parts.pop();
    currentPath = parts.join('/');
    loadContent();
}

async function uploadFile() {
    const fileInput = document.getElementById('fileInput');
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    await fetch(`/api/upload?path=${currentPath}`, {
        method: 'POST',
        body: formData
    });
    loadContent();
}

window.onload = loadContent;