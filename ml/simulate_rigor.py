import pandas as pd
import numpy as np
import math

# Configurações Atuais (Exemplo Gênero: Brazil/Pop)
CURRENT_RANGES = {
    'bpm': (100, 135),
    'energy': (0.6, 0.9),
    'danceability': (0.7, 0.9),
    'loudness': (-8, -4)
}
CURRENT_WEIGHTS = {
    'bpm': 15,
    'energy': 25,
    'danceability': 35,
    'loudness': 10,
    'brightness': 10,
    'dynamic_variation': 5
}

# Configurações PROPOSTAS (Iron Rule)
IRON_RANGES = {
    'bpm': (110, 130), # Mais estreito
    'energy': (0.7, 0.85), # Mais estreito
    'danceability': (0.75, 0.9), # Mais estreito
    'loudness': (-7, -5) # Mais estreito
}

def current_normalize(value, ideal_min, ideal_max):
    if value < ideal_min:
        distance = ideal_min - value
        penalty = min(distance / ideal_min, 1) if ideal_min != 0 else 0
        return 1 - penalty
    elif value > ideal_max:
        distance = value - ideal_max
        penalty = min(distance / ideal_max, 1) if ideal_max != 0 else 0
        return 1 - penalty
    return 1.0

def iron_normalize(value, ideal_min, ideal_max):
    if value < ideal_min:
        distance = ideal_min - value
        # Penalidade QUADRÁTICA (muito mais severa)
        penalty = (distance / (ideal_min * 0.5))**2 # Dobra a velocidade da queda
        return max(0, 1 - penalty)
    elif value > ideal_max:
        distance = value - ideal_max
        penalty = (distance / (ideal_max * 0.5))**2
        return max(0, 1 - penalty)
    return 1.0

def calculate_score(row, ranges, weights, methodology='current'):
    scores = {}
    
    # BPM
    bpm_val = row['tempo']
    if methodology == 'current':
        scores['bpm'] = current_normalize(bpm_val, *ranges['bpm'])
        if 120 <= bpm_val <= 128: scores['bpm'] = min(scores['bpm'] * 1.1, 1.0) # BÔNUS
    else:
        scores['bpm'] = iron_normalize(bpm_val, *ranges['bpm']) # SEM BÔNUS
        
    # Energy
    scores['energy'] = current_normalize(row['energy'], *ranges['energy']) if methodology == 'current' else iron_normalize(row['energy'], *ranges['energy'])
    
    # Danceability
    dance_val = row['danceability']
    if methodology == 'current':
        scores['danceability'] = current_normalize(dance_val, *ranges['danceability'])
        if dance_val > 0.8: scores['danceability'] = min(scores['danceability'] * 1.15, 1.0) # BÔNUS
    else:
        scores['danceability'] = iron_normalize(dance_val, *ranges['danceability']) # SEM BÔNUS
        
    # Loudness
    scores['loudness'] = current_normalize(row['loudness'], *ranges['loudness']) if methodology == 'current' else iron_normalize(row['loudness'], *ranges['loudness'])
    
    # Outros (Padrão 0.7 para simulação já que não temos no CSV)
    scores['brightness'] = 0.7
    scores['dynamic_variation'] = 0.7
    
    total = 0
    for k, v in scores.items():
        total += v * weights.get(k, 0)
        
    return int(round(total))

# Carregar Dados
df = pd.read_csv('c:/Users/jonat/Documents/Novo HIT/ml/datasets/massive_brazil_spotify.csv')
hits = df[df['popularity'] > 75].head(10) # 10 Hits Reais

results = []
for idx, row in hits.iterrows():
    curr = calculate_score(row, CURRENT_RANGES, CURRENT_WEIGHTS, 'current')
    iron = calculate_score(row, IRON_RANGES, CURRENT_WEIGHTS, 'iron')
    results.append({
        'Musica': row['track_name'],
        'Popularidade': row['popularity'],
        'Score Atual': curr,
        'Score Iron (Rigor)': iron,
        'Diferença': iron - curr
    })

res_df = pd.DataFrame(results)
print("\n--- TESTE RETROATIVO: HITS REAIS DO SPOTIFY ---")
print(res_df.to_string(index=False))

# Músicas Menos Populares
low_hits = df[df['popularity'] < 30].head(5)
low_results = []
for idx, row in low_hits.iterrows():
    curr = calculate_score(row, CURRENT_RANGES, CURRENT_WEIGHTS, 'current')
    iron = calculate_score(row, IRON_RANGES, CURRENT_WEIGHTS, 'iron')
    low_results.append({
        'Musica': row['track_name'],
        'Popularidade': row['popularity'],
        'Score Atual': curr,
        'Score Iron': iron
    })

print("\n--- TESTE RETROATIVO: MÚSICAS NÃO-POPULARES ---")
print(pd.DataFrame(low_results).to_string(index=False))
