// Configuração da API
const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
const API_URL = '/api';

// Estado da aplicação
let selectedFiles = []; // Lista de arquivos File
let availableGenres = []; // Lista de gêneros da API
let analysisResults = []; // [{ filename: string, features: {}, predictions: { genreId: predictionObj } }]

// Elementos DOM
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const selectedFilesContainer = document.getElementById('selectedFilesContainer');
const filesList = document.getElementById('filesList');
const genresGrid = document.getElementById('genresGrid');
const analyzeBtn = document.getElementById('analyzeBtn');

const uploadSection = document.getElementById('uploadSection');
const loadingSection = document.getElementById('loadingSection');
const progressFill = document.getElementById('progressFill');
const loadingText = document.getElementById('loadingText');

const batchResultsSection = document.getElementById('batchResultsSection');
const comparisonTable = document.getElementById('comparisonTable');
const tableHeader = document.getElementById('tableHeader');
const tableBody = document.getElementById('tableBody');

const resultsSection = document.getElementById('resultsSection');
const backToBatchBtn = document.getElementById('backToBatchBtn');
const individualTitle = document.getElementById('individualTitle');
const newBatchBtn = document.getElementById('newBatchBtn');
const newAnalysisBtn = document.getElementById('newAnalysisBtn');
const suggestGenresBtn = document.getElementById('suggestGenresBtn');

// Event Listeners
dropZone.addEventListener('click', () => fileInput.click());
dropZone.addEventListener('dragover', handleDragOver);
dropZone.addEventListener('dragleave', handleDragLeave);
dropZone.addEventListener('drop', handleDrop);
fileInput.addEventListener('change', handleFileSelect);
analyzeBtn.addEventListener('click', startBatchAnalysis);
newBatchBtn.addEventListener('click', resetApp);
newAnalysisBtn.addEventListener('click', resetApp);
backToBatchBtn.addEventListener('click', showBatchResults);
suggestGenresBtn.addEventListener('click', suggestBestGenres);

// Drag and Drop Handlers
function handleDragOver(e) { e.preventDefault(); dropZone.classList.add('drag-over'); }
function handleDragLeave(e) { e.preventDefault(); dropZone.classList.remove('drag-over'); }
function handleDrop(e) {
    e.preventDefault();
    dropZone.classList.remove('drag-over');
    handleFiles(e.dataTransfer.files);
}
function handleFileSelect(e) { handleFiles(e.target.files); }

// File Handling
function handleFiles(files) {
    const validTypes = ['audio/mpeg', 'audio/wav', 'audio/ogg', 'audio/flac', 'audio/x-m4a'];
    const validExtensions = ['.mp3', '.wav', '.ogg', '.flac', '.m4a'];

    const newFiles = Array.from(files).filter(file => {
        const ext = '.' + file.name.split('.').pop().toLowerCase();
        return validTypes.includes(file.type) || validExtensions.includes(ext);
    });

    if (newFiles.length === 0 && files.length > 0) {
        alert('Nenhum formato de áudio válido selecionado.');
        return;
    }

    // Limita a 10 músicas
    selectedFiles = [...selectedFiles, ...newFiles].slice(0, 10);
    renderFilesList();
    validateInputs();
}

function renderFilesList() {
    filesList.innerHTML = '';
    selectedFiles.forEach((file, index) => {
        const item = document.createElement('div');
        item.className = 'file-item';
        item.innerHTML = `
            <div class="file-item-info">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="opacity: 0.6"><path d="M9 18V5l12-2v13"></path><circle cx="6" cy="18" r="3"></circle><circle cx="18" cy="16" r="3"></circle></svg>
                <span class="file-item-name" title="${file.name}">${file.name}</span>
            </div>
            <button class="btn-remove" onclick="removeFile(${index})">✕</button>
        `;
        filesList.appendChild(item);
    });

    selectedFilesContainer.style.display = selectedFiles.length > 0 ? 'block' : 'none';
}

window.removeFile = function (index) {
    selectedFiles.splice(index, 1);
    renderFilesList();
    validateInputs();
};

function validateInputs() {
    const selectedGenres = getSelectedGenres();
    analyzeBtn.disabled = selectedFiles.length === 0 || selectedGenres.length === 0;
    suggestGenresBtn.disabled = selectedFiles.length === 0;
}

function getSelectedGenres() {
    const checkboxes = genresGrid.querySelectorAll('input:checked');
    return Array.from(checkboxes).map(cb => cb.value);
}

async function suggestBestGenres() {
    if (selectedFiles.length === 0) {
        alert('Por favor, selecione uma música primeiro.');
        return;
    }

    suggestGenresBtn.disabled = true;
    suggestGenresBtn.textContent = '⏳ Analisando...';

    try {
        const allGenreScores = {}; // Acumula scores de todas as músicas

        // Analisa cada música
        for (let i = 0; i < selectedFiles.length; i++) {
            const file = selectedFiles[i];

            // Atualiza progresso
            suggestGenresBtn.textContent = `⏳ ${i + 1}/${selectedFiles.length}...`;

            // Extrai features da música
            const formData = new FormData();
            formData.append('audio', file);
            formData.append('genres[]', 'mpb_rock'); // Dummy para extrair features

            const response = await fetch(`${API_URL}/analyze`, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                console.warn(`Erro ao analisar ${file.name}, pulando...`);
                continue;
            }

            const data = await response.json();
            const features = data.features;

            // Calcula scores para esta música
            const genreScores = calculateGenreScores(features);

            // Acumula scores
            for (const [genre, score] of Object.entries(genreScores)) {
                if (!allGenreScores[genre]) allGenreScores[genre] = 0;
                allGenreScores[genre] += score;
            }
        }

        // Calcula média dos scores
        const avgScores = {};
        for (const [genre, totalScore] of Object.entries(allGenreScores)) {
            avgScores[genre] = totalScore / selectedFiles.length;
        }

        // Ordena por score médio e pega os top 2
        const sortedGenres = Object.entries(avgScores)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 2)
            .map(([id]) => id);

        // Desmarca todos
        genresGrid.querySelectorAll('input').forEach(cb => cb.checked = false);

        // Marca os top 2
        sortedGenres.forEach(genreId => {
            const checkbox = document.getElementById(`genre_${genreId}`);
            if (checkbox) checkbox.checked = true;
        });

        validateInputs();

        // Mostra mensagem de sucesso
        const genreNames = sortedGenres.map(id => {
            const genre = availableGenres.find(g => g.id === id);
            return genre ? genre.name : id;
        }).join(' e ');

        const songText = selectedFiles.length === 1 ? '1 música' : `${selectedFiles.length} músicas`;
        suggestGenresBtn.textContent = `✅ ${genreNames}`;
        setTimeout(() => {
            suggestGenresBtn.textContent = '✨ Sugerir Gêneros';
            suggestGenresBtn.disabled = false;
        }, 3000);

    } catch (error) {
        console.error('Erro ao sugerir gêneros:', error);
        alert('Erro ao analisar músicas. Tente novamente.');
        suggestGenresBtn.textContent = '✨ Sugerir Gêneros';
        suggestGenresBtn.disabled = false;
    }
}

function calculateGenreScores(features) {
    const genreScores = {};

    // R&B Trap: BPM baixo + ALTA speechiness + energia alta + NÃO acústico
    genreScores['rnb_trap'] = 0;
    if (features.bpm < 95) genreScores['rnb_trap'] += 30;
    if (features.speechiness > 0.2) genreScores['rnb_trap'] += 35; // Aumentado threshold
    if (features.energy > 0.7) genreScores['rnb_trap'] += 20;
    if (features.danceability > 0.6) genreScores['rnb_trap'] += 15;
    // PENALIDADES para evitar falsos positivos
    if (features.acousticness > 0.5) genreScores['rnb_trap'] -= 40; // Trap não é acústico
    if (features.speechiness < 0.15) genreScores['rnb_trap'] -= 30; // Trap TEM que ter rap

    // R&B Pop: BPM médio + baixa speechiness + valence positiva
    genreScores['rnb_pop'] = 0;
    if (features.bpm >= 95 && features.bpm <= 120) genreScores['rnb_pop'] += 25;
    if (features.speechiness < 0.15) genreScores['rnb_pop'] += 20;
    if (features.valence > 0.5) genreScores['rnb_pop'] += 25;
    if (features.danceability > 0.6) genreScores['rnb_pop'] += 15;
    if (features.acousticness > 0.4) genreScores['rnb_pop'] += 10; // R&B Pop pode ser acústico

    // MPB Rock: Alta energia + loudness alto
    genreScores['mpb_rock'] = 0;
    if (features.energy > 0.6) genreScores['mpb_rock'] += 30;
    if (features.loudness > -7) genreScores['mpb_rock'] += 25;
    if (features.bpm > 110) genreScores['mpb_rock'] += 20;
    if (features.acousticness < 0.4) genreScores['mpb_rock'] += 15;

    // MPB Indie: Acústico + valence médio + speechiness BAIXA
    genreScores['mpb_indie'] = 0;
    if (features.acousticness > 0.5) genreScores['mpb_indie'] += 35;
    if (features.valence >= 0.4 && features.valence <= 0.7) genreScores['mpb_indie'] += 25;
    if (features.bpm >= 95 && features.bpm <= 120) genreScores['mpb_indie'] += 20;
    if (features.energy >= 0.4 && features.energy <= 0.65) genreScores['mpb_indie'] += 15;
    if (features.speechiness < 0.15) genreScores['mpb_indie'] += 15; // Indie tem pouca fala

    // Sertanejo: BPM alto + danceability alta
    genreScores['sertanejo'] = 0;
    if (features.bpm > 120) genreScores['sertanejo'] += 30;
    if (features.danceability > 0.7) genreScores['sertanejo'] += 25;
    if (features.valence > 0.6) genreScores['sertanejo'] += 20;
    if (features.acousticness > 0.4) genreScores['sertanejo'] += 15;

    // Pagode: BPM médio-alto + danceability alta + acústico
    genreScores['pagode'] = 0;
    if (features.bpm >= 100 && features.bpm <= 130) genreScores['pagode'] += 25;
    if (features.danceability > 0.7) genreScores['pagode'] += 30;
    if (features.acousticness > 0.5) genreScores['pagode'] += 20;
    if (features.valence > 0.6) genreScores['pagode'] += 15;

    // Samba: Similar ao pagode mas mais acústico + speechiness baixa
    genreScores['samba'] = 0;
    if (features.bpm >= 90 && features.bpm <= 120) genreScores['samba'] += 30;
    if (features.acousticness > 0.6) genreScores['samba'] += 35;
    if (features.danceability > 0.6) genreScores['samba'] += 20;
    if (features.valence > 0.5) genreScores['samba'] += 15;
    if (features.speechiness < 0.15) genreScores['samba'] += 10; // Samba tem pouca fala

    // Forró: BPM específico + danceability
    genreScores['forro'] = 0;
    if (features.bpm >= 110 && features.bpm <= 140) genreScores['forro'] += 30;
    if (features.danceability > 0.7) genreScores['forro'] += 25;
    if (features.acousticness > 0.4) genreScores['forro'] += 20;

    // Pop Urban: Energia + danceability + produção moderna
    genreScores['pop_urban_brasil'] = 0;
    if (features.energy > 0.6) genreScores['pop_urban_brasil'] += 25;
    if (features.danceability > 0.65) genreScores['pop_urban_brasil'] += 25;
    if (features.loudness > -6) genreScores['pop_urban_brasil'] += 20;
    if (features.valence > 0.5) genreScores['pop_urban_brasil'] += 15;

    // Garante que scores negativos viram 0
    for (const genre in genreScores) {
        genreScores[genre] = Math.max(0, genreScores[genre]);
    }

    return genreScores;
}

// Batch Analysis
async function startBatchAnalysis() {
    const genreIds = getSelectedGenres();
    if (selectedFiles.length === 0 || genreIds.length === 0) return;

    uploadSection.style.display = 'none';
    loadingSection.style.display = 'block';
    analysisResults = [];

    try {
        for (let i = 0; i < selectedFiles.length; i++) {
            const file = selectedFiles[i];

            // Log para debug
            console.log(`>>> Iniciando análise de: ${file.name}`);

            // Atualiza progresso (mínimo 5% no início para dar feedback)
            const baseProgress = (i / selectedFiles.length) * 100;
            progressFill.style.width = `${Math.max(5, baseProgress)}%`;
            loadingText.textContent = `Analisando: ${file.name} (${i + 1}/${selectedFiles.length})`;

            const formData = new FormData();
            formData.append('audio', file);
            genreIds.forEach(id => formData.append('genres[]', id));

            try {
                const response = await fetch(`${API_URL}/analyze`, {
                    method: 'POST',
                    body: formData
                });

                if (!response.ok) {
                    const errBody = await response.json();
                    throw new Error(errBody.error || `Erro HTTP ${response.status}`);
                }

                const data = await response.json();
                console.log(`<<< Sucesso: ${file.name}`, data);

                analysisResults.push({
                    originalName: file.name,
                    features: data.features,
                    predictions: data.predictions
                });
            } catch (error) {
                console.error(`Falha no arquivo ${file.name}:`, error);
                alert(`Erro ao analisar "${file.name}":\n${error.message}`);
                // Continua para o próximo arquivo mesmo com erro
            }
        }
    } catch (criticalError) {
        console.error("Erro crítico no lote:", criticalError);
        alert("Ocorreu um erro inesperado que interrompeu o processamento.");
    } finally {
        progressFill.style.width = '100%';
        loadingSection.style.display = 'none';

        if (analysisResults.length > 0) {
            showBatchResults();
        } else {
            uploadSection.style.display = 'block';
            resetApp();
        }
    }
}

function showBatchResults() {
    loadingSection.style.display = 'none';
    resultsSection.style.display = 'none';
    batchResultsSection.style.display = 'block';

    renderComparisonTable();
}

function renderComparisonTable() {
    const selectedGenres = getSelectedGenres();

    // Header - Agora com coluna de Estilo Ideal
    tableHeader.innerHTML = '<th>Arquivo</th>';
    selectedGenres.forEach(genreId => {
        const genre = availableGenres.find(g => g.id === genreId);
        const th = document.createElement('th');
        th.textContent = genre ? genre.name : genreId;
        tableHeader.appendChild(th);
    });

    const thBest = document.createElement('th');
    thBest.innerHTML = 'Match IA <small style="display:block; font-size: 9px; opacity: 0.5;">(Estilo Ideal)</small>';
    tableHeader.appendChild(thBest);

    // Body
    tableBody.innerHTML = '';
    analysisResults.forEach((result, songIndex) => {
        const tr = document.createElement('tr');

        // Nome da música - Mais elegante
        const tdName = document.createElement('td');
        tdName.innerHTML = `<div style="max-width: 180px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; font-weight: 500;">${result.originalName}</div>`;
        tr.appendChild(tdName);

        // Scores por gênero e cálculo do melhor
        let maxScore = -1;
        let bestGenreId = null;

        selectedGenres.forEach(genreId => {
            const td = document.createElement('td');
            const prediction = result.predictions[genreId];
            if (prediction) {
                const score = prediction.hit_score;

                if (score > maxScore) {
                    maxScore = score;
                    bestGenreId = genreId;
                }

                td.className = 'score-cell';
                td.innerHTML = `<span class="score-badge" style="background: ${getScoreColor(score)}11; color: ${getScoreColor(score)}">${score}</span>`;
                td.onclick = () => showIndividualDetail(songIndex, genreId);
            } else {
                td.textContent = '-';
            }
            tr.appendChild(td);
        });

        // Célula do Melhor Match
        const tdBest = document.createElement('td');
        if (bestGenreId) {
            const genreName = getGenreName(bestGenreId);
            tdBest.innerHTML = `
                <div class="best-match-pill" onclick="showIndividualDetail(${songIndex}, '${bestGenreId}')">
                    <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"></polyline></svg>
                    ${genreName}
                </div>
            `;
        } else {
            tdBest.textContent = '-';
        }
        tr.appendChild(tdBest);

        tableBody.appendChild(tr);
    });
}

function getScoreColor(score) {
    if (score >= 80) return '#10b981';
    if (score >= 60) return '#3b82f6';
    if (score >= 40) return '#f59e0b';
    return '#ef4444';
}

function showIndividualDetail(songIndex, genreId) {
    const result = analysisResults[songIndex];
    const prediction = result.predictions[genreId];

    batchResultsSection.style.display = 'none';
    resultsSection.style.display = 'block';
    backToBatchBtn.style.display = 'block';

    individualTitle.textContent = `Análise: ${result.originalName}`;
    document.getElementById('currentAnalysisSongName').textContent = `Estilo: ${getGenreName(genreId)}`;

    displayResults({
        features: result.features,
        prediction: prediction
    });
}

function getGenreName(id) {
    const g = availableGenres.find(x => x.id === id);
    return g ? g.name : id;
}

function displayResults(data) {
    const { features, prediction } = data;

    console.log('[DEBUG] displayResults chamado');
    console.log('[DEBUG] prediction:', prediction);
    console.log('[DEBUG] hit_averages:', prediction.hit_averages);
    console.log('[DEBUG] createThermometerChart existe?', typeof createThermometerChart);

    document.getElementById('scoreDescription').textContent = prediction.hit_description || '';

    // Chama funções do visualizations.js e locais
    if (typeof animateScore === 'function') animateScore(prediction.hit_score);

    // SEMPRE usa termômetro E radar
    if (typeof createRadarChart === 'function') {
        createRadarChart(features, prediction.hit_averages);
    }

    if (typeof createThermometerChart === 'function') {
        createThermometerChart(features, prediction.hit_averages);
    }

    displayFeatures(features);
    displayRecommendations(prediction.recommendations);
}

function animateScore(target) {
    const el = document.getElementById('scoreNumber');
    let current = 0;
    const step = target / 30;
    const interval = setInterval(() => {
        current += step;
        if (current >= target) {
            el.textContent = Math.round(target);
            clearInterval(interval);
        } else {
            el.textContent = Math.round(current);
        }
    }, 20);
}

function displayFeatures(features) {
    const grid = document.getElementById('featuresGrid');
    grid.innerHTML = '';

    const labels = {
        'bpm': 'BPM (Tempo)',
        'energy': 'Energia',
        'danceability': 'Dançabilidade',
        'valence': 'Positividade',
        'acousticness': 'Acusticidade',
        'instrumentalness': 'Instrumentalidade',
        'liveness': 'Presença de Público',
        'speechiness': 'Fala/Rap',
        'loudness': 'Loudness (Volume)',
        'key': 'Tonalidade'
    };

    for (const [key, val] of Object.entries(features)) {
        if (!labels[key]) continue;

        const item = document.createElement('div');
        item.className = 'feature-item';

        let displayVal = val;
        if (typeof val === 'number') {
            if (key === 'loudness') {
                displayVal = val.toFixed(1) + ' dB';
            } else if (val >= 0 && val <= 1 && key !== 'bpm' && key !== 'loudness') {
                // Converte features 0-1 para porcentagem (energy, danceability, valence, acousticness, instrumentalness, liveness, speechiness)
                displayVal = (val * 100).toFixed(0) + '%';
            } else {
                displayVal = val.toFixed(1);
            }
        }

        item.innerHTML = `
            <div class="feature-label">${labels[key]}</div>
            <div class="feature-value">${displayVal}</div>
        `;
        grid.appendChild(item);
    }
}

function displayRecommendations(recommendations) {
    const list = document.getElementById('recommendationsList');
    list.innerHTML = '';

    if (!recommendations || recommendations.length === 0) {
        list.innerHTML = '<p>Nenhuma recomendação específica para este estilo.</p>';
        return;
    }

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
    selectedFiles = [];
    analysisResults = [];
    renderFilesList();
    uploadSection.style.display = 'block';
    loadingSection.style.display = 'none';
    batchResultsSection.style.display = 'none';
    resultsSection.style.display = 'none';
    validateInputs();
}

// Inicialização
window.addEventListener('load', async () => {
    try {
        const genresResponse = await fetch(`${API_URL}/genres`);
        const genresData = await genresResponse.json();
        availableGenres = genresData.genres;

        if (availableGenres) {
            genresGrid.innerHTML = '';
            availableGenres.forEach(genre => {
                const item = document.createElement('div');
                item.className = 'genre-checkbox-item';
                item.innerHTML = `
                    <input type="checkbox" id="genre_${genre.id}" value="${genre.id}" onchange="validateInputs()">
                    <label for="genre_${genre.id}" class="genre-checkbox-label">
                        ${genre.name}
                    </label>
                `;
                genresGrid.appendChild(item);
            });
        }
    } catch (error) {
        console.warn('Erro ao carregar gêneros:', error);
    }
});
