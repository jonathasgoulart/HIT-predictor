// Quick Wins UX Improvements
// Adicione este código ao final do app.js existente

// ========================================
// 1. TOOLTIPS EXPLICATIVOS
// ========================================

// Função para criar tooltip
function createTooltip(element, text) {
    const tooltip = document.createElement('div');
    tooltip.className = 'custom-tooltip';
    tooltip.textContent = text;
    tooltip.style.cssText = `
        position: absolute;
        background: rgba(31, 41, 55, 0.95);
        color: white;
        padding: 12px 16px;
        border-radius: 8px;
        font-size: 13px;
        line-height: 1.5;
        max-width: 300px;
        z-index: 1000;
        opacity: 0;
        pointer-events: none;
        transition: opacity 0.2s;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    `;

    element.style.position = 'relative';
    element.style.cursor = 'help';

    element.addEventListener('mouseenter', () => {
        document.body.appendChild(tooltip);
        const rect = element.getBoundingClientRect();
        tooltip.style.left = rect.left + 'px';
        tooltip.style.top = (rect.bottom + 8) + 'px';
        setTimeout(() => tooltip.style.opacity = '1', 10);
    });

    element.addEventListener('mouseleave', () => {
        tooltip.style.opacity = '0';
        setTimeout(() => tooltip.remove(), 200);
    });
}

// Adicionar tooltips aos scores
function addScoreTooltips() {
    // Tooltip no score principal
    const scoreNumber = document.getElementById('scoreNumber');
    if (scoreNumber && currentAnalysisData) {
        const genre = currentAnalysisData.genre || 'mpb';
        const accuracy = getGenreAccuracy(genre);
        const realProb = estimateRealProbability(currentAnalysisData.hit_score, accuracy);

        createTooltip(scoreNumber,
            `Score ${currentAnalysisData.hit_score}% = Qualidade técnica muito boa\n\n` +
            `Chance real de hit: ~${realProb}%\n` +
            `(Baseado em modelo com ${accuracy}% de accuracy)`
        );
    }
}

// Obter accuracy do gênero
function getGenreAccuracy(genre) {
    const accuracies = {
        'sertanejo': 71,
        'samba': 71,
        'pagode': 63,
        'pop_urban_brasil': 63,
        'rnb_brasil': 60,
        'mpb': 54,
        'forro': 50
    };
    return accuracies[genre] || 55;
}

// Estimar probabilidade real
function estimateRealProbability(score, accuracy) {
    // Fórmula: prob_real = (score/100) * (accuracy/100) * 100
    const normalized = score / 100;
    const adjusted = normalized * (accuracy / 100);
    return Math.round(adjusted * 100);
}

// ========================================
// 2. MENSAGENS DE ERRO MELHORADAS
// ========================================

function showError(type, details = '') {
    const errorMessages = {
        'file_too_large': {
            title: 'Arquivo muito grande',
            message: 'O arquivo excede o limite de 50MB. Por favor, comprima o áudio ou use um arquivo menor.',
            icon: '⚠️'
        },
        'invalid_format': {
            title: 'Formato inválido',
            message: 'Use apenas arquivos MP3, WAV, FLAC, OGG ou M4A.',
            icon: '❌'
        },
        'analysis_failed': {
            title: 'Análise falhou',
            message: 'Não foi possível analisar o arquivo. Verifique se o áudio está corrompido ou tente novamente.',
            icon: '⚠️'
        },
        'network_error': {
            title: 'Erro de conexão',
            message: 'Não foi possível conectar ao servidor. Verifique sua conexão e tente novamente.',
            icon: '🔌'
        },
        'no_genres': {
            title: 'Selecione um gênero',
            message: 'Por favor, selecione pelo menos um estilo musical para análise.',
            icon: 'ℹ️'
        }
    };

    const error = errorMessages[type] || {
        title: 'Erro',
        message: details || 'Ocorreu um erro inesperado.',
        icon: '❌'
    };

    // Criar modal de erro
    const modal = document.createElement('div');
    modal.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10000;
        animation: fadeIn 0.2s;
    `;

    modal.innerHTML = `
        <div style="
            background: white;
            padding: 2rem;
            border-radius: 12px;
            max-width: 400px;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
            animation: slideUp 0.3s;
        ">
            <div style="font-size: 3rem; text-align: center; margin-bottom: 1rem;">
                ${error.icon}
            </div>
            <h3 style="
                font-size: 1.25rem;
                font-weight: 700;
                margin-bottom: 0.5rem;
                text-align: center;
                color: #1f2937;
            ">${error.title}</h3>
            <p style="
                color: #6b7280;
                text-align: center;
                margin-bottom: 1.5rem;
                line-height: 1.6;
            ">${error.message}</p>
            <button onclick="this.closest('div[style*=fixed]').remove()" style="
                width: 100%;
                padding: 0.75rem;
                background: #2563eb;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: 600;
                cursor: pointer;
                transition: background 0.2s;
            " onmouseover="this.style.background='#1d4ed8'" 
               onmouseout="this.style.background='#2563eb'">
                Entendi
            </button>
        </div>
    `;

    document.body.appendChild(modal);

    // Auto-remover após 10 segundos
    setTimeout(() => modal.remove(), 10000);
}

// Adicionar CSS para animações
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    @keyframes slideUp {
        from { transform: translateY(20px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
`;
document.head.appendChild(style);

// ========================================
// 3. EXPORT PARA PDF (Simples)
// ========================================

function exportResultsToPDF() {
    if (!currentAnalysisData) return;

    // Por enquanto, criar um relatório em texto que pode ser impresso
    const reportWindow = window.open('', '_blank');
    reportWindow.document.write(`
        <!DOCTYPE html>
        <html>
        <head>
            <title>Relatório Hit Predictor - ${currentAnalysisData.filename}</title>
            <style>
                body {
                    font-family: 'Arial', sans-serif;
                    max-width: 800px;
                    margin: 2rem auto;
                    padding: 2rem;
                    line-height: 1.6;
                }
                h1 { color: #1a1a1a; border-bottom: 3px solid #2563eb; padding-bottom: 0.5rem; }
                h2 { color: #404040; margin-top: 2rem; }
                .score { font-size: 3rem; color: #2563eb; font-weight: bold; text-align: center; margin: 2rem 0; }
                .feature { display: flex; justify-content: space-between; padding: 0.5rem; border-bottom: 1px solid #e5e7eb; }
                .recommendation { padding: 1rem; margin: 0.5rem 0; border-left: 4px solid #f59e0b; background: #fffbeb; }
                @media print {
                    body { margin: 0; padding: 1rem; }
                }
            </style>
        </head>
        <body>
            <h1>🎵 Relatório de Análise - Hit Predictor</h1>
            <p><strong>Música:</strong> ${currentAnalysisData.filename}</p>
            <p><strong>Gênero:</strong> ${getGenreName(currentAnalysisData.genre)}</p>
            <p><strong>Data:</strong> ${new Date().toLocaleDateString('pt-BR')}</p>
            
            <h2>Potencial de Hit</h2>
            <div class="score">${currentAnalysisData.hit_score}/100</div>
            <p style="text-align: center; color: #6b7280;">
                ${currentAnalysisData.hit_score >= 70 ? 'Excelente potencial!' :
            currentAnalysisData.hit_score >= 50 ? 'Bom potencial' : 'Potencial médio'}
            </p>
            
            <h2>Características da Música</h2>
            ${Object.entries(currentAnalysisData.features || {}).map(([key, value]) => `
                <div class="feature">
                    <span><strong>${key.toUpperCase()}:</strong></span>
                    <span>${typeof value === 'number' ? value.toFixed(2) : value}</span>
                </div>
            `).join('')}
            
            <h2>Recomendações</h2>
            ${(currentAnalysisData.recommendations || []).map(rec => `
                <div class="recommendation">
                    <strong>${rec.category}:</strong> ${rec.message}
                </div>
            `).join('') || '<p>Nenhuma recomendação específica.</p>'}
            
            <hr style="margin: 2rem 0;">
            <p style="text-align: center; color: #6b7280; font-size: 0.9rem;">
                Hit Predictor © 2026 - Análise gerada automaticamente
            </p>
            
            <script>
                window.onload = () => {
                    setTimeout(() => window.print(), 500);
                };
            </script>
        </body>
        </html>
    `);
    reportWindow.document.close();
}

// Adicionar botão de export nos resultados
function addExportButton() {
    const resultsSection = document.getElementById('resultsSection');
    if (!resultsSection || document.getElementById('exportBtn')) return;

    const exportBtn = document.createElement('button');
    exportBtn.id = 'exportBtn';
    exportBtn.className = 'btn-secondary';
    exportBtn.style.cssText = `
        margin-top: 1rem;
        width: 100%;
        padding: 0.75rem;
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 6px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s;
    `;
    exportBtn.innerHTML = '📄 Baixar Relatório (PDF)';
    exportBtn.onclick = exportResultsToPDF;

    const newAnalysisBtn = document.getElementById('newAnalysisBtn');
    if (newAnalysisBtn) {
        newAnalysisBtn.parentNode.insertBefore(exportBtn, newAnalysisBtn);
    }
}

// ========================================
// INTEGRAÇÃO
// ========================================

// Variável global para armazenar dados da análise atual
let currentAnalysisData = null;

// Hook na função displayResults existente
const originalDisplayResults = window.displayResults;
if (originalDisplayResults) {
    window.displayResults = function (data) {
        currentAnalysisData = data;
        originalDisplayResults(data);
        addScoreTooltips();
        addExportButton();
    };
}

console.log('✅ Quick Wins UX carregados!');
