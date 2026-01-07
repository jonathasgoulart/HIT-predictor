// Visualizações usando Chart.js

let scoreGaugeChart = null;
let radarChartInstance = null;

function createScoreGauge(score) {
    const canvas = document.getElementById('scoreGauge');
    const ctx = canvas.getContext('2d');

    // Destruir chart anterior se existir
    if (scoreGaugeChart) {
        scoreGaugeChart.destroy();
    }

    // Determinar cor baseada no score
    let color;
    if (score >= 80) {
        color = '#10b981'; // Verde
    } else if (score >= 60) {
        color = '#3b82f6'; // Azul
    } else if (score >= 40) {
        color = '#f59e0b'; // Amarelo
    } else {
        color = '#ef4444'; // Vermelho
    }

    scoreGaugeChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            datasets: [{
                data: [score, 100 - score],
                backgroundColor: [color, 'rgba(255, 255, 255, 0.1)'],
                borderWidth: 0,
                circumference: 180,
                rotation: 270
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            cutout: '75%',
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    enabled: false
                }
            }
        }
    });
}

function createRadarChart(scores) {
    const canvas = document.getElementById('radarChart');
    const ctx = canvas.getContext('2d');

    // Destruir chart anterior se existir
    if (radarChartInstance) {
        radarChartInstance.destroy();
    }

    // Preparar dados
    const labels = [];
    const data = [];

    const labelMap = {
        'bpm': 'BPM',
        'energy': 'Energia',
        'danceability': 'Dançabilidade',
        'loudness': 'Loudness',
        'duration': 'Duração',
        'brightness': 'Brilho',
        'dynamic_variation': 'Variação'
    };

    for (const [key, value] of Object.entries(scores)) {
        if (labelMap[key]) {
            labels.push(labelMap[key]);
            data.push(value);
        }
    }

    radarChartInstance = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Score',
                data: data,
                backgroundColor: 'rgba(139, 92, 246, 0.2)',
                borderColor: 'rgba(139, 92, 246, 1)',
                borderWidth: 2,
                pointBackgroundColor: 'rgba(139, 92, 246, 1)',
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: 'rgba(139, 92, 246, 1)',
                pointRadius: 4,
                pointHoverRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                r: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        stepSize: 20,
                        color: 'rgba(255, 255, 255, 0.5)',
                        backdropColor: 'transparent'
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    pointLabels: {
                        color: 'rgba(255, 255, 255, 0.8)',
                        font: {
                            size: 12,
                            weight: '600'
                        }
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    borderColor: 'rgba(139, 92, 246, 1)',
                    borderWidth: 1,
                    padding: 12,
                    displayColors: false,
                    callbacks: {
                        label: function (context) {
                            return context.parsed.r.toFixed(1) + '/100';
                        }
                    }
                }
            }
        }
    });
}
