# Sistema de Treinamento ML - Música Brasileira

Sistema completo para coletar dados do Spotify e treinar modelos de predição de hits específicos para música brasileira.

## 🎯 Objetivo

Treinar modelos ML específicos para gêneros brasileiros:
- **MPB/Nova MPB**
- **R&B Brasil**
- Futuramente: Funk, Sertanejo, Pagode, Pop Brasil

## 📊 Estratégia de Dataset

### Balanceamento
- **500 músicas populares** (hits confirmados, popularidade > 70)
- **500 músicas médias** (1K-1M plays estimados, popularidade 30-70)
- **Total**: 1000 músicas por gênero

### Critério de Hit
- **Hit** (label=1): Popularidade Spotify > 70
- **Não-Hit** (label=0): Popularidade 30-70

---

## 🚀 Setup Rápido

### 1. Instalar Dependências

```bash
cd ml
pip install -r requirements.txt
```

### 2. Configurar Spotify API

1. Acesse: https://developer.spotify.com/dashboard
2. Faça login (gratuito)
3. Crie um novo App
4. Copie **Client ID** e **Client Secret**

Execute o configurador:

```bash
python spotify_auth.py
```

Cole suas credenciais quando solicitado.

### 3. Coletar Dados

```bash
python data_collector.py
```

Isso irá:
- Buscar playlists de MPB e R&B Brasil
- Coletar 1000 músicas de cada gênero
- Salvar em `datasets/mpb_dataset.csv` e `datasets/rnb_brasil_dataset.csv`

### 4. Treinar Modelos

```bash
python train_model.py
```

Modelos treinados serão salvos em `models/`

---

## 📁 Estrutura

```
ml/
├── spotify_auth.py          # Autenticação Spotify
├── playlist_finder.py       # Busca de playlists
├── data_collector.py        # Coleta de dados
├── train_model.py           # Treinamento ML
├── requirements.txt         # Dependências
├── .env                     # Credenciais (criado automaticamente)
├── datasets/                # Datasets coletados
│   ├── mpb_dataset.csv
│   └── rnb_brasil_dataset.csv
└── models/                  # Modelos treinados
    ├── mpb_RandomForest_*.pkl
    └── rnb_brasil_RandomForest_*.pkl
```

---

## 🎵 Playlists Utilizadas

### MPB/Nova MPB
- MPB Hits (oficial Spotify)
- Nova MPB (oficial Spotify)
- MPB Clássica

### R&B Brasil
- R&B Brasil (oficial Spotify)
- Soul Brasil

---

## 🤖 Modelos

### Random Forest (padrão)
- **n_estimators**: 100 árvores
- **max_depth**: 10
- **Features**: BPM, energia, dançabilidade, valência, etc.

### Gradient Boosting (alternativo)
- **n_estimators**: 100
- **learning_rate**: 0.1

---

## 📊 Features Utilizadas

1. **bpm** - Batidas por minuto
2. **energy** - Energia da música
3. **danceability** - Dançabilidade
4. **valence** - Positividade/valência
5. **acousticness** - Acústico
6. **instrumentalness** - Instrumental
7. **liveness** - Ao vivo
8. **speechiness** - Fala/rap
9. **loudness** - Volume
10. **duration_ms** - Duração

---

## 📈 Métricas Esperadas

- **Accuracy**: > 75%
- **Precision**: > 70%
- **Recall**: > 70%
- **F1 Score**: > 72%

---

## 🔧 Uso Avançado

### Coletar Apenas Um Gênero

```python
from spotify_auth import SpotifyAuth
from data_collector import DataCollector

auth = SpotifyAuth()
collector = DataCollector(auth)

# Apenas MPB
df = collector.collect_balanced_dataset('mpb')
collector.save_dataset(df, 'mpb_dataset.csv')
```

### Treinar com Hiperparâmetros Customizados

```python
from train_model import ModelTrainer

trainer = ModelTrainer('datasets/mpb_dataset.csv')
trainer.load_dataset()
trainer.prepare_data()

# Random Forest customizado
trainer.train_random_forest(n_estimators=200, max_depth=15)
metrics = trainer.evaluate()
trainer.save_model()
```

---

## 🐛 Troubleshooting

### Erro de Autenticação
```
ValueError: Credenciais do Spotify não encontradas
```
**Solução**: Execute `python spotify_auth.py` e configure suas credenciais

### Rate Limit do Spotify
```
429 Too Many Requests
```
**Solução**: O collector já tem delays automáticos. Se persistir, aguarde alguns minutos.

### Dataset Pequeno
```
Menos de 1000 músicas coletadas
```
**Solução**: Normal para gêneros menores. O modelo ainda funcionará, mas com menos dados.

---

## 📝 Próximos Passos

1. ✅ Coletar dados MPB e R&B Brasil
2. ✅ Treinar modelos iniciais
3. [ ] Integrar com backend da aplicação
4. [ ] Adicionar seletor de gênero no frontend
5. [ ] Expandir para outros gêneros (Funk, Sertanejo, etc.)

---

## 🤝 Contribuindo

Para adicionar novos gêneros:

1. Adicione playlists em `playlist_finder.py`:
```python
CURATED_PLAYLISTS = {
    'novo_genero': [
        'playlist_id_1',
        'playlist_id_2'
    ]
}
```

2. Execute coleta:
```bash
python data_collector.py
```

3. Treine modelo:
```bash
python train_model.py
```

---

**Desenvolvido para análise de música brasileira 🇧🇷**
