"""
Recria datasets sintéticos e mescla com dados reais caso existam
"""
import pandas as pd
import numpy as np
import os

def create_and_merge():
    # 1. Carrega dados reais que acabamos de extrair
    real_data = {}
    genres = ['sertanejo', 'forro', 'pagode', 'samba', 'pop_urban_brasil', 'mpb']
    
    for genre in genres:
        path = f'ml/datasets/kaggle_{genre}_ml.csv'
        if os.path.exists(path):
            try:
                df = pd.read_csv(path)
                real_data[genre] = df
                print(f"Carregado real {genre}: {len(df)} musicas")
            except:
                real_data[genre] = pd.DataFrame()
        else:
            real_data[genre] = pd.DataFrame()

    # 2. Gera sintéticos
    # Mesma lógica do create_brazilian_datasets.py
    
    genre_profiles = {
        'sertanejo': {'bpm': (120, 140), 'energy': (0.75, 0.9), 'sample_size': 20},
        'forro': {'bpm': (130, 170), 'energy': (0.7, 0.95), 'sample_size': 30}, # Aumentado pois não tem reais
        'pagode': {'bpm': (90, 125), 'energy': (0.6, 0.9), 'sample_size': 20},
        'samba': {'bpm': (90, 125), 'energy': (0.6, 0.9), 'sample_size': 25}, # Aumentado
        'pop_urban_brasil': {'bpm': (115, 130), 'energy': (0.65, 0.85), 'sample_size': 10},
        'mpb': {'bpm': (80, 120), 'energy': (0.4, 0.7), 'sample_size': 15}
    }
    
    columns = [
        'track_name', 'artist_name', 'bpm', 'energy', 'danceability',
        'valence', 'acousticness', 'instrumentalness', 'liveness',
        'speechiness', 'loudness', 'is_hit'
    ]
    
    for genre, profile in genre_profiles.items():
        # Se já tem muitos dados reais (>50), não precisa de sintético
        if len(real_data.get(genre, [])) > 50:
            print(f"Pulinado sintético para {genre} (já tem {len(real_data[genre])} reais)")
            continue
            
        print(f"Gerando sintéticos complementares para {genre}...")
        
        data = []
        sample_size = profile['sample_size']
        
        for i in range(sample_size):
            is_hit = 1 if i < sample_size // 2 else 0
            
            if is_hit:
                bpm = np.random.normal(np.mean(profile['bpm']), 5)
                energy = np.random.normal(np.mean(profile['energy']), 0.05)
            else:
                bpm = np.random.uniform(*profile['bpm'])
                energy = np.random.uniform(0.3, 1.0)
                
            data.append({
                'track_name': f'{genre.capitalize()} Sample {i+1}',
                'artist_name': f'Generic {genre.capitalize()}',
                'bpm': float(bpm),
                'energy': float(energy),
                'danceability': float(np.random.uniform(0.5, 0.9)),
                'valence': float(np.random.uniform(0.4, 0.9)),
                'acousticness': float(np.random.uniform(0.1, 0.6)),
                'instrumentalness': 0.0,
                'liveness': 0.1,
                'speechiness': 0.05,
                'loudness': -8.0,
                'is_hit': is_hit
            })
            
        df_synth = pd.DataFrame(data, columns=columns)
        
        # Mescla
        if not real_data[genre].empty:
            # Garante colunas compatíveis
            cols_real = [c for c in columns if c in real_data[genre].columns]
            df_final = pd.concat([real_data[genre][cols_real], df_synth[cols_real]], ignore_index=True)
            # Preenche colunas faltantes no real
            for col in columns:
                if col not in df_final.columns:
                    df_final[col] = 0.5 # Valor default seguro
        else:
            df_final = df_synth
            
        # Salva
        output_file = f'ml/datasets/kaggle_{genre}_ml.csv'
        df_final.to_csv(output_file, index=False)
        print(f"Salvo mesclado: {output_file} ({len(df_final)} total)")

if __name__ == "__main__":
    create_and_merge()
