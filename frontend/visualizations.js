// Visualizações usando Chart.js

let radarChartInstance = null;

function createRadarChart(userScores, hitAverages) {
    const canvas = document.getElementById('radarChart');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    // Destruir chart anterior se existir
    if (radarChartInstance) {
        radarChartInstance.destroy();
    }

    // Preparar dados
    const labels = [];
    const userData = [];
    const hitData = [];

    const labelMap = {
        'danceability': 'Groove',
        'energy': 'Energia',
        'valence': 'Vibe',
        'acousticness': 'Acústico',
        'speechiness': 'Voz/Fala',
        'instrumentalness': 'Inst.',
        'bpm': 'BPM'
    };

    const keys = ['danceability', 'energy', 'valence', 'acousticness', 'speechiness', 'instrumentalness'];

    keys.forEach(key => {
        labels.push(labelMap[key]);
        userData.push(userScores[key] * 100);
        hitData.push((hitAverages ? (hitAverages[key] || 0.5) : 0.5) * 100);
    });

    radarChartInstance = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Sua Música',
                    data: userData,
                    backgroundColor: 'rgba(37, 99, 235, 0.2)',
                    borderColor: 'rgba(37, 99, 235, 1)',
                    borderWidth: 3,
                    pointBackgroundColor: 'rgba(37, 99, 235, 1)',
                    pointBorderColor: '#fff',
                    pointRadius: 4,
                    fill: true
                },
                {
                    label: 'Média de Hits',
                    data: hitData,
                    backgroundColor: 'rgba(239, 68, 68, 0.1)',
                    borderColor: 'rgba(239, 68, 68, 0.8)',
                    borderWidth: 2,
                    borderDash: [5, 5],
                    pointBackgroundColor: 'rgba(239, 68, 68, 1)',
                    pointRadius: 0,
                    fill: true
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                r: {
                    beginAtZero: true,
                    max: 100,
                    min: 0,
                    ticks: { display: false, stepSize: 20 },
                    grid: { color: 'rgba(0, 0, 0, 0.05)' },
                    pointLabels: {
                        font: { size: 12, weight: '700' },
                        color: '#1f2937'
                    }
                }
            },
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: { boxWidth: 12, font: { size: 11, weight: '600' } }
                }
            }
        }
    });
}

// Novo gráfico de termômetro comparativo
function createThermometerChart(userFeatures, hitAverages) {
    console.log('[THERMO] createThermometerChart');

    const container = document.getElementById('thermometerContainer');
    if (!container) return;

    container.innerHTML = ''; // Limpa conteúdo anterior

    // Se não houver médias dos hits, não exibe nada
    if (!hitAverages) {
        container.innerHTML = '<p style="text-align: center; color: #6b7280;">Dados de comparação indisponíveis</p>';
        return;
    }

    // Glossário detalhado de features
    const glossary = {
        'danceability': 'Mede o quão adequada a música é para dançar, baseado em elementos como tempo, estabilidade do ritmo, força da batida e regularidade.',
        'energy': 'Representa a intensidade e atividade percebida da música. Músicas rápidas e barulhentas têm energia alta.',
        'valence': 'Mede a positividade musical transmitida. Valores altos indicam músicas alegres e positivas.',
        'acousticness': 'Indica a probabilidade da música ser acústica (sem instrumentos eletrônicos).',
        'liveness': 'Detecta a presença de público na gravação.',
        'instrumentalness': 'Prevê se a música contém vocais. 100% significa puramente instrumental.',
        'speechiness': 'Detecta a presença de palavras faladas. Rap fica entre 30-70%.'
    };

    const features = [
        { key: 'danceability', label: 'Dançabilidade', unit: '%', scale: 100 },
        { key: 'energy', label: 'Energia', unit: '%', scale: 100 },
        { key: 'valence', label: 'Positividade', unit: '%', scale: 100 },
        { key: 'acousticness', label: 'Acusticidade', unit: '%', scale: 100 },
        { key: 'speechiness', label: 'Fala/Rap', unit: '%', scale: 100 }
    ];

    features.forEach(feature => {
        const userValue = userFeatures[feature.key] || 0;
        const hitValue = hitAverages[feature.key] || 0.5;

        // Normaliza para 0-100
        const userPercent = userValue * feature.scale;
        const hitPercent = hitValue * feature.scale;

        const item = document.createElement('div');
        item.className = 'thermometer-item';

        const comparisonText = getComparisonText(userPercent, hitPercent);

        item.innerHTML = `
            <div class="thermometer-label">
                ${feature.label}
                <span class="info-icon" data-tooltip="${glossary[feature.key]}">ℹ️</span>
            </div>
            <div class="thermometer-bar-container">
                <div class="thermometer-bar" style="width: ${userPercent}%">
                    <span class="thermometer-value">${userPercent.toFixed(0)}%</span>
                </div>
                <div class="thermometer-marker" style="left: ${hitPercent}%">
                    <span class="thermometer-hit-label">Hits: ${hitPercent.toFixed(0)}%</span>
                </div>
            </div>
            <div class="thermometer-comparison">
                ${comparisonText}
            </div>
        `;

        container.appendChild(item);
    });
}

function getComparisonText(userValue, hitValue) {
    const diff = userValue - hitValue;

    if (Math.abs(diff) < 5) {
        return `<span class="comparison-good">✓ Dentro da média dos hits</span>`;
    } else if (diff > 0) {
        return `<span class="comparison-high">↑ ${diff.toFixed(0)}% acima dos hits</span>`;
    } else {
        return `<span class="comparison-low">↓ ${Math.abs(diff).toFixed(0)}% abaixo dos hits</span>`;
    }
}
