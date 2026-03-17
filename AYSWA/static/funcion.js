console.log("Sistema de Encuestas cargado correctamente");

// función para gestionar la elaboración de encuestas
const questionsContainer = document.getElementById('questions');
const newQuestionInput = document.getElementById('new-question');
const addBtn = document.getElementById('add-btn');
const saveBtn = document.getElementById('save-btn');

let questionCount = 0;

function createQuestionCard(questionText = '') {
    questionCount += 1;
    const card = document.createElement('div');
    card.className = 'question-card';

    const header = document.createElement('div');
    header.className = 'question-header';

    const number = document.createElement('span');
    number.className = 'question-number';
    number.textContent = questionCount + '.';

    const textSpan = document.createElement('span');
    textSpan.className = 'question-text';
    textSpan.textContent = questionText;

    header.appendChild(number);
    header.appendChild(textSpan);

    const textarea = document.createElement('textarea');
    textarea.placeholder = 'Escribe la respuesta aquí...';

    const deleteIcon = document.createElement('span');
    deleteIcon.className = 'delete';
    deleteIcon.textContent = '🗑️';
    deleteIcon.addEventListener('click', () => {
        questionsContainer.removeChild(card);
        refreshNumbers();
    });

    card.appendChild(header);
    card.appendChild(deleteIcon);
    card.appendChild(textarea);

    return card;
}

function refreshNumbers() {
    questionCount = 0;
    Array.from(questionsContainer.children).forEach((card) => {
        questionCount += 1;
        const numElem = card.querySelector('.question-number');
        if (numElem) numElem.textContent = questionCount + '.';
    });
}

addBtn.addEventListener('click', () => {
    const text = newQuestionInput.value.trim();
    if (text === '') return;
    const card = createQuestionCard(text);
    questionsContainer.appendChild(card);
    newQuestionInput.value = '';
});

saveBtn.addEventListener('click', () => {
    // recolectar preguntas y posibles respuestas
    const cards = Array.from(questionsContainer.querySelectorAll('.question-card'));
    const resultado = cards.map(card => {
        const q = card.querySelector('.question-text')?.textContent || '';
        const a = card.querySelector('textarea')?.value.trim() || '';
        return { pregunta: q, respuesta: a };
    });
    console.log('Encuesta guardada:', resultado);
    alert('Encuesta guardada (ver consola para detalles).');
});

// inicialización con preguntas de ejemplo
function initializeDefaults() {
    const preguntas = [
        '¿Cómo calificarías tu experiencia general?',
        '¿Qué aspectos te gustan más?',
        '¿Qué mejorarías?'
    ];
    preguntas.forEach(p => {
        const card = createQuestionCard(p);
        questionsContainer.appendChild(card);
    });
}

initializeDefaults();