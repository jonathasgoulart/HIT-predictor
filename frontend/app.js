// Configuração da API
const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
const API_URL = isLocal ? 'http://localhost:5000/api' : '/api';


// Estado da aplicação
let selectedFile = null;

// Elementos DOM
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const selectedFileDiv = document.getElementById('selectedFile');
const fileName = document.getElementById('fileName');
const fileSize = document.getElementById('fileSize');
const removeFileBtn = document.getElementById('removeFile');
const analyzeBtn = document.getElementById('analyzeBtn');
const uploadSection = document.getElementById('uploadSection');
const loadingSection = document.getElementById('loadingSection');
const resultsSection = document.getElementById('resultsSection');
const newAnalysisBtn = document.getElementById('newAnalysisBtn');
const genreSelect = document.getElementById('genreSelect');

// Event Listeners
dropZone.addEventListener('click', () => fileInput.click());
dropZone.addEventListener('dragover', handleDragOver);
dropZone.addEventListener('dragleave', handleDragLeave);
dropZone.addEventListener('drop', handleDrop);
fileInput.addEventListener('change', handleFileSelect);
removeFileBtn.addEventListener('click', clearFile);
analyzeBtn.addEventListener('click', analyzeAudio);
newAnalysisBtn.addEventListener('click', resetApp);

// Drag and Drop Handlers
function handleDragOver(e) {
    e.preventDefault();
    dropZone.classList.add('drag-over');
}

function handleDragLeave(e) {
    e.preventDefault();
    dropZone.classList.remove('drag-over');
}

function handleDrop(e) {
    e.preventDefault();
    dropZone.classList.remove('drag-over');

    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
}

function handleFileSelect(e) {
    const files = e.target.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
}

// File Handling
function handleFile(file) {
    // Validar tipo de arquivo
    const validTypes = ['audio/mpeg', 'audio/wav', 'audio/ogg', 'audio/flac', 'audio/x-m4a'];
    const validExtensions = ['.mp3', '.wav', '.ogg', '.flac', '.m4a'];

    const fileExtension = '.' + file.name.split('.').pop().toLowerCase();

    if (!validTypes.includes(file.type) && !validExtensions.includes(fileExtension)) {
        alert('Formato de arquivo não suportado. Use MP3, WAV, OGG, FLAC ou M4A.');
        return;
    }

    // Validar tamanho (50MB)
    const maxSize = 50 * 1024 * 1024;
    if (file.size > maxSize) {
        alert('Arquivo muito grande. O tamanho máximo é 50MB.');
        return;
    }

    selectedFile = file;
    displaySelectedFile(file);
}

function displaySelectedFile(file) {
    fileName.textContent = file.name;
    fileSize.textContent = formatFileSize(file.size);

    selectedFileDiv.style.display = 'flex';
    dropZone.style.display = 'none';
    analyzeBtn.disabled = false;
}

function clearFile() {
    selectedFile = null;
    fileInput.value = '';
    selectedFileDiv.style.display = 'none';
    dropZone.style.display = 'block';
    analyzeBtn.disabled = true;
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// Analysis
async function analyzeAudio() {
    if (!selectedFile) return;

    // Mostrar loading
    uploadSection.style.display = 'none';
    loadingSection.style.display = 'block';
    resultsSection.style.display = 'none';

    try {
        // Preparar FormData
        const formData = new FormData();
        formData.append('audio', selectedFile);
        formData.append('genre', genreSelect.value);

        // Enviar para API
        const response = await fetch(`${API_URL}/analyze`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Erro ao analisar áudio');
        }

        const data = await response.json();

        // Exibir resultados
        displayResults(data);

    } catch (error) {
        console.error('Erro:', error);
        alert(`Erro ao analisar música: ${error.message}\n\nVerifique se o servidor backend está rodando em ${API_URL}`);
        resetApp();
    }
}

function displayResults(data) {
    const { features, prediction } = data;

    // Esconder loading, mostrar resultados
    loadingSection.style.display = 'none';
    resultsSection.style.display = 'block';

    // Animar score
    animateScore(prediction.hit_score);

    // Criar gauge chart
    createScoreGauge(prediction.hit_score);

    // Criar radar chart
    createRadarChart(prediction.individual_scores);

    // Exibir features
    displayFeatures(features);

    // Exibir recomendações
    displayRecommendations(prediction.recommendations);

    // Scroll suave para resultados
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function animateScore(targetScore) {
    const scoreElement = document.getElementById('scoreNumber');
    const descriptionElement = document.getElementById('scoreDescription');

    let currentScore = 0;
    const duration = 2000; // 2 segundos
    const increment = targetScore / (duration / 16); // 60 FPS

    const animation = setInterval(() => {
        currentScore += increment;
        if (currentScore >= targetScore) {
            currentScore = targetScore;
            clearInterval(animation);
        }
        scoreElement.textContent = Math.round(currentScore);
    }, 16);

    // Descrição baseada no score
    if (targetScore >= 80) {
        descriptionElement.textContent = '🔥 Excelente! Grande potencial de hit!';
        descriptionElement.style.color = '#10b981';
    } else if (targetScore >= 60) {
        descriptionElement.textContent = '✨ Muito bom! Com alguns ajustes pode ser um hit.';
        descriptionElement.style.color = '#3b82f6';
    } else if (targetScore >= 40) {
        descriptionElement.textContent = '💡 Bom começo. Veja as recomendações para melhorar.';
        descriptionElement.style.color = '#f59e0b';
    } else {
        descriptionElement.textContent = '🎯 Precisa de trabalho. Confira as sugestões abaixo.';
        descriptionElement.style.color = '#ef4444';
    }
}

function displayFeatures(features) {
    const grid = document.getElementById('featuresGrid');
    grid.innerHTML = '';

    const featureLabels = {
        'bpm': { label: 'BPM', format: (v) => Math.round(v) },
        'energy': { label: 'Energia', format: (v) => (v * 100).toFixed(1) + '%' },
        'danceability': { label: 'Dançabilidade', format: (v) => (v * 100).toFixed(1) + '%' },
        'loudness': { label: 'Loudness', format: (v) => v.toFixed(1) + ' dB' },
        'duration': { label: 'Duração', format: (v) => formatDuration(v) },
        'key': { label: 'Tonalidade', format: (v) => v },
        'brightness': { label: 'Brilho', format: (v) => Math.round(v) + ' Hz' }
    };

    for (const [key, config] of Object.entries(featureLabels)) {
        if (features[key] !== undefined) {
            const item = document.createElement('div');
            item.className = 'feature-item';
            item.innerHTML = `
                <div class="feature-label">${config.label}</div>
                <div class="feature-value">${config.format(features[key])}</div>
            `;
            grid.appendChild(item);
        }
    }
}

function formatDuration(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
}

function displayRecommendations(recommendations) {
    const list = document.getElementById('recommendationsList');
    list.innerHTML = '';

    recommendations.forEach(rec => {
        const item = document.createElement('div');
        item.className = `recommendation-item ${rec.priority}`;
        item.innerHTML = `
            <div class="recommendation-category">
                ${rec.category}
                <span class="priority-badge ${rec.priority}">${rec.priority}</span>
            </div>
            <div class="recommendation-message">${rec.message}</div>
        `;
        list.appendChild(item);
    });
}

function resetApp() {
    clearFile();
    uploadSection.style.display = 'block';
    loadingSection.style.display = 'none';
    resultsSection.style.display = 'none';
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Verificar e Carregar Gêneros ao iniciar
window.addEventListener('load', async () => {
    try {
        // Health check
        const healthResponse = await fetch(`${API_URL}/health`);
        if (healthResponse.ok) {
            console.log('✅ API conectada com sucesso');
        }

        // Carregar gêneros
        const genresResponse = await fetch(`${API_URL}/genres`);
        const genresData = await genresResponse.json();

        if (genresData.genres) {
            genreSelect.innerHTML = '';
            genresData.genres.forEach(genre => {
                const option = document.createElement('option');
                option.value = genre.id;
                option.textContent = genre.name + (genre.has_ml_model ? ' (IA)' : '');
                genreSelect.appendChild(option);
            });
        }
    } catch (error) {
        console.warn('⚠️ Erro ao conectar com API:', error);
    }
});
