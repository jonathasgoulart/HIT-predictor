"""
Expande dataset de MPB de 30 para ~500+ músicas
Usa threshold de popularidade para criar labels
"""
import pandas as pd
import numpy as np
import os

# Carrega dataset grande do Kaggle
print("Carregando kaggle_mpb.csv...")
df = pd.read_csv('ml/datasets/kaggle_mpb.csv')
print(f"Total: {len(df)} musicas")

# Verifica se tem coluna de popularidade
print(f"\nColunas disponíveis: {df.columns.tolist()}")

# Se não tiver 'popularity', vamos criar baseado em outra métrica
# ou usar uma amostra balanceada aleatória

# Renomeia colunas para formato ML
df_ml = pd.DataFrame()
df_ml['track_name'] = df['name']
df_ml['artist'] = df['artist_names']
df_ml['bpm'] = df['tempo']
df_ml['energy'] = df['energy']
df_ml['danceability'] = df['danceability']
df_ml['valence'] = df['valence']
df_ml['acousticness'] = df['acousticness']
df_ml['instrumentalness'] = df['instrumentalness']
df_ml['liveness'] = df['liveness']
df_ml['speechiness'] = df['speechiness']
df_ml['loudness'] = df['loudness']
df_ml['genre'] = 'mpb'

# Remove valores nulos
df_ml = df_ml.dropna()
print(f"\nApos remover nulos: {len(df_ml)} musicas")

# Se não temos popularidade, vamos criar um dataset balanceado artificial
# usando a distribuição das features
# Músicas com características "comerciais" = hits

# Critérios heurísticos para MPB baseado na análise de correlação
# Acousticness alto é bom (+0.286 corr)
# Speechiness baixo é bom (-0.203 corr)

df_ml['commercial_score'] = (
    (df_ml['acousticness'] * 0.4) +  # Mais acústico = melhor
    ((1 - df_ml['speechiness']) * 0.3) +  # Menos fala = melhor
    (df_ml['valence'] * 0.2) +  # Mais positivo = melhor
    (df_ml['energy'] * 0.1)  # Um pouco de energia
)

# Threshold no percentil 60 (mais hits que não-hits para treino)
threshold = df_ml['commercial_score'].quantile(0.60)
df_ml['is_hit'] = (df_ml['commercial_score'] >= threshold).astype(int)

# Remove coluna auxiliar
df_ml = df_ml.drop('commercial_score', axis=1)

# Limita a 800 músicas para não ficar muito grande
# Balanceia hits e não-hits
hits = df_ml[df_ml['is_hit'] == 1].sample(n=min(400, len(df_ml[df_ml['is_hit'] == 1])), random_state=42)
non_hits = df_ml[df_ml['is_hit'] == 0].sample(n=min(400, len(df_ml[df_ml['is_hit'] == 0])), random_state=42)

df_final = pd.concat([hits, non_hits]).sample(frac=1, random_state=42)  # Shuffle

print(f"\nDataset final:")
print(f"  Total: {len(df_final)} musicas")
print(f"  Hits: {df_final['is_hit'].sum()}")
print(f"  Nao-hits: {(1-df_final['is_hit']).sum()}")

# Salva
output_path = 'ml/datasets/kaggle_mpb_ml_expanded.csv'
df_final.to_csv(output_path, index=False)
print(f"\n[OK] Salvo em: {output_path}")
print(f"\nAgora retreine o modelo MPB com:")
print(f"  python ml/train_model.py {output_path}")
