# 🎵 Hit Predictor

Ferramenta de análise musical que prevê o potencial de uma música se tornar um hit usando análise de áudio e machine learning.

## 🌟 Características

- **Análise Completa de Áudio**: Extrai BPM, energia, tonalidade, dançabilidade e muito mais
- **Score de Hit Potential**: Calcula uma pontuação de 0-100 baseada em características de hits populares
- **Visualizações Interativas**: Gráficos dinâmicos com Chart.js
- **Interface Premium**: Design moderno com glassmorphism e animações suaves
- **Recomendações Personalizadas**: Sugestões específicas para melhorar sua música

## 🚀 Tecnologias

### Backend
- **Python 3.8+**
- **Flask**: API REST
- **Librosa**: Análise de áudio
- **NumPy/SciPy**: Processamento numérico

### Frontend
- **HTML5/CSS3/JavaScript**
- **Chart.js**: Visualizações
- **Design moderno**: Gradientes, glassmorphism, animações

## 📦 Instalação

### 1. Backend

```bash
cd backend
pip install -r requirements.txt
```

### 2. Frontend

Não requer instalação. Apenas um navegador moderno.

## ▶️ Como Usar

### 1. Iniciar o Backend

```bash
cd backend
python api.py
```

O servidor estará disponível em `http://localhost:5000`

### 2. Abrir o Frontend

Abra o arquivo `frontend/index.html` em seu navegador, ou use um servidor local:

```bash
cd frontend
python -m http.server 8000
```

Acesse `http://localhost:8000`

### 3. Analisar uma Música

1. Arraste e solte um arquivo de áudio (MP3, WAV, OGG, FLAC, M4A)
2. Clique em "Analisar Música"
3. Aguarde o processamento
4. Visualize os resultados!

## 📊 O Que é Analisado

### Características Extraídas

- **BPM (Tempo)**: Batidas por minuto
- **Energia**: Intensidade geral da música
- **Dançabilidade**: Regularidade rítmica
- **Loudness**: Volume percebido
- **Tonalidade**: Key musical (C, D, E, etc.)
- **Brilho Espectral**: Frequências altas
- **Variação Dinâmica**: Mudanças ao longo do tempo
- **MFCCs**: Características timbrais

### Score de Hit Potential

O score é calculado baseado em:

- **Ranges ideais** de características de hits populares
- **Pesos ponderados** para cada característica
- **Análise heurística** de padrões conhecidos

Características mais importantes:
- Dançabilidade (25%)
- Energia (20%)
- BPM (15%)
- Outros (40%)

## 🎯 Interpretação dos Resultados

- **80-100**: 🔥 Excelente potencial de hit!
- **60-79**: ✨ Muito bom, pequenos ajustes podem melhorar
- **40-59**: 💡 Bom começo, veja as recomendações
- **0-39**: 🎯 Precisa de trabalho significativo

## 🔧 Estrutura do Projeto

```
Novo HIT/
├── backend/
│   ├── api.py                 # API Flask
│   ├── audio_analyzer.py      # Extração de features
│   ├── hit_predictor.py       # Modelo de predição
│   ├── requirements.txt       # Dependências Python
│   └── uploads/               # Arquivos temporários
│
└── frontend/
    ├── index.html             # Estrutura HTML
    ├── styles.css             # Estilos e design
    ├── app.js                 # Lógica da aplicação
    └── visualizations.js      # Gráficos Chart.js
```

## 🎨 Design

Interface moderna com:
- **Dark theme** elegante
- **Glassmorphism** effects
- **Gradientes vibrantes** (roxo/azul)
- **Animações suaves** e micro-interações
- **Responsivo** para mobile e desktop

## 🔮 Futuras Melhorias

- [ ] Modelo ML treinado com dataset real de hits
- [ ] Análise de letras (sentiment analysis)
- [ ] Comparação com músicas similares
- [ ] Histórico de análises
- [ ] Export de relatórios PDF
- [ ] API pública com autenticação

## 📝 Notas Técnicas

### Modelo de Predição

Atualmente usa **heurísticas baseadas em padrões** de hits populares. Para um modelo mais preciso, seria necessário:

1. Dataset de milhares de músicas com labels (hit/não-hit)
2. Treinamento com algoritmos de ML (Random Forest, XGBoost, etc.)
3. Validação cruzada e otimização de hiperparâmetros

### Limitações

- Análise limitada aos primeiros 3 minutos da música
- Não analisa letras ou contexto cultural
- Baseado em padrões de música pop/dance ocidental
- Não considera fatores externos (marketing, timing, etc.)

## 📄 Licença

Projeto de demonstração - Uso livre para fins educacionais

## 🤝 Contribuições

Sugestões e melhorias são bem-vindas!

---

**Desenvolvido com ❤️ para músicos e produtores**
