# 📚 Datasets Públicos de Música Brasileira - Catálogo

## ✅ Datasets Recomendados

### 1. **Brazilian Hit Songs Dataset (2014-2019)** ⭐ ALTAMENTE RECOMENDADO

**Link**: https://github.com/tocaestudio/Music_3DataSets

**Descrição**:
- **881-882 músicas** brasileiras populares
- **Classificadas** como hit/não-hit
- **Período**: Janeiro 2014 - Maio 2019
- **3.215 features** estatísticas extraídas

**Features Incluídas**:
- ✅ Audio features completos (via Essentia package)
- ✅ Análise de melodia vocal predominante
- ✅ Análise semântica musical
- ✅ 74 características estatisticamente relevantes

**Vantagens**:
- ✅ Já classificado como hit/não-hit
- ✅ Específico para música brasileira
- ✅ Grande quantidade de features
- ✅ Gratuito no GitHub

**Como usar**:
```bash
git clone https://github.com/tocaestudio/Music_3DataSets
```

---

### 2. **Brazilian Music Genre Classification Database**

**Descrição**:
- **1.907 registros**
- **11 gêneros** brasileiros específicos

**Gêneros**:
- Axé, Bossa Nova, Brega, Choro, Forró
- Frevo, Funk Carioca, Maracatu
- Música Sertaneja, Pagode, Samba

**Fonte**: Dados do Spotify

**Vantagens**:
- ✅ Classificação automática de gêneros
- ✅ Dados reais do Spotify
- ✅ Foco em gêneros brasileiros tradicionais

---

### 3. **Brazil Regional Spotify Charts (2021-2023)** ✅ JÁ ESTAMOS USANDO

**Link**: https://www.kaggle.com/datasets/filipeasm/brazil-regional-spotify-charts

**Status**: ✅ **Já baixado e em uso!**

**Descrição**:
- 5.190 músicas únicas
- 487 gêneros
- 17 cidades brasileiras
- Audio features completos

---

### 4. **SAMBASET - Historical Samba Dataset**

**Descrição**:
- Dataset específico de **samba de enredo**
- Gravações históricas
- Anotações para análise computacional

**Vantagens**:
- ✅ Cultura-específico
- ✅ Foco em samba autêntico
- ✅ Evita mistura com bossa nova/pagode

---

### 5. **Vagalume Brazilian Platform Dataset**

**Descrição**:
- **96.458 músicas**
- **15.310 artistas**

**Inclui**:
- Letras das músicas
- Anotações de gênero
- Metadados
- Audio features

**Vantagens**:
- ✅ Muito grande (96k músicas!)
- ✅ Plataforma brasileira
- ✅ Inclui letras

---

## 🎯 Recomendação de Uso

### Opção A: **Brazilian Hit Songs (2014-2019)** ⭐ MELHOR PARA VOCÊ

**Por quê?**:
1. ✅ **Já classificado** como hit/não-hit (economiza trabalho!)
2. ✅ **881 músicas** - muito mais que os 132/116 atuais
3. ✅ **Features prontos** para ML
4. ✅ **Gratuito** no GitHub
5. ✅ **Específico** para predição de hits

**Próximos passos**:
```bash
# 1. Clonar repositório
git clone https://github.com/tocaestudio/Music_3DataSets

# 2. Processar datasets
# 3. Treinar modelos
# 4. Comparar com modelos atuais
```

### Opção B: **Combinar Múltiplos Datasets**

Usar:
- Kaggle (atual) - 5.190 músicas
- GitHub Hit Songs - 881 músicas
- = **6.071 músicas** no total!

---

## 📊 Comparação Rápida

| Dataset | Músicas | Hit/Não-Hit | Audio Features | Gratuito |
|---------|---------|-------------|----------------|----------|
| **Kaggle (atual)** | 5.190 | ❌ (heurística) | ✅ | ✅ |
| **GitHub Hit Songs** | 881 | ✅ (real) | ✅ | ✅ |
| **Genre Classification** | 1.907 | ❌ | ✅ | ✅ |
| **Vagalume** | 96.458 | ❌ | ✅ | ✅ |

---

## 🚀 Ação Recomendada

**Baixar o dataset do GitHub** (881 músicas com classificação hit/não-hit real):

```bash
cd ml/datasets
git clone https://github.com/tocaestudio/Music_3DataSets github_hits
```

Depois processar e combinar com os dados do Kaggle!

**Quer que eu faça isso agora?** 🎵
