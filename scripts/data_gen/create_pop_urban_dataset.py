"""
Cria dataset específico para Pop/Urban Brasil
Características: Mix de Pop comercial com elementos urbanos brasileiros
"""
import pandas as pd
import numpy as np
import os

np.random.seed(42)

# Características do Pop/Urban Brasil
# BPM: 115-130 (mais rápido que R&B, mais comercial)
# Energia: 0.65-0.85 (alta energia, comercial)
# Dançabilidade: 0.75-0.9 (muito dançante)
# Valence: 0.6-0.8 (positivo, comercial)

columns = [
    'track_name', 'artist_name', 'bpm', 'energy', 'danceability',
    'valence', 'acousticness', 'instrumentalness', 'liveness',
    'speechiness', 'loudness', 'is_hit'
]

data = []
sample_size = 40  # Maior que os outros para ter mais variedade

print("Criando dataset para Pop/Urban Brasil...")

for i in range(sample_size):
    is_hit = 1 if i < sample_size // 2 else 0
    
    # Hits tendem a estar no sweet spot
    if is_hit:
        bpm = np.random.normal(122, 4)  # Centrado em 122 BPM
        energy = np.random.normal(0.75, 0.05)
        danceability = np.random.normal(0.82, 0.04)
        valence = np.random.normal(0.7, 0.05)
        acousticness = np.random.normal(0.25, 0.08)
        loudness = np.random.normal(-6, 0.5)
    else:
        # Não-hits têm mais variação
        bpm = np.random.uniform(100, 140)
        energy = np.random.uniform(0.4, 0.95)
        danceability = np.random.uniform(0.5, 0.95)
        valence = np.random.uniform(0.3, 0.9)
        acousticness = np.random.uniform(0.0, 0.6)
        loudness = np.random.uniform(-10, -4)
    
    # Outras features
    instrumentalness = np.random.uniform(0.0, 0.05)  # Muito vocal
    liveness = np.random.uniform(0.08, 0.25)
    speechiness = np.random.uniform(0.05, 0.2)  # Pode ter rap/fala
    
    data.append({
        'track_name': f'Pop Urban Song {i+1}',
        'artist_name': f'Artist {i+1}',
        'bpm': np.clip(bpm, 60, 200),
        'energy': np.clip(energy, 0, 1),
        'danceability': np.clip(danceability, 0, 1),
        'valence': np.clip(valence, 0, 1),
        'acousticness': np.clip(acousticness, 0, 1),
        'instrumentalness': instrumentalness,
        'liveness': liveness,
        'speechiness': speechiness,
        'loudness': np.clip(loudness, -20, 0),
        'is_hit': is_hit
    })

# Salva CSV
df = pd.DataFrame(data, columns=columns)
output_file = 'ml/datasets/kaggle_pop_urban_brasil_ml.csv'
os.makedirs('ml/datasets', exist_ok=True)
df.to_csv(output_file, index=False)

print(f"OK Dataset criado: {output_file}")
print(f"  - {len(df)} musicas ({sum(df['is_hit']==1)} hits, {sum(df['is_hit']==0)} nao-hits)")
print(f"  - BPM medio: {df['bpm'].mean():.1f}")
print(f"  - Energia media: {df['energy'].mean():.2f}")
print(f"  - Dancabilidade media: {df['danceability'].mean():.2f}")
