"""
Script para baixar e processar datasets de gêneros brasileiros do Kaggle
Gêneros: Sertanejo, Forró, Pagode, Samba

Dataset fonte: Spotify Songs Dataset (Kaggle)
https://www.kaggle.com/datasets/
"""
import pandas as pd
import os
import sys

# Instruções para o usuário
INSTRUCTIONS = """
================================================================================
COLETA DE DADOS - GÊNEROS BRASILEIROS
================================================================================

Este script processa dados de música brasileira para criar datasets específicos.

OPÇÃO 1: Usar dados do Kaggle (Recomendado)
--------------------------------------------
1. Acesse: https://www.kaggle.com/datasets/
2. Procure por "Spotify Songs Dataset" ou "Brazilian Music Dataset"
3. Baixe o CSV e salve em: ml/datasets/raw/
4. Renomeie para: brazilian_music_raw.csv
5. Execute este script novamente

OPÇÃO 2: Criar dados manualmente
---------------------------------
Vou criar datasets de exemplo com estrutura correta.
Você pode preencher com dados reais depois.

================================================================================
"""

def create_sample_datasets():
    """Cria datasets de exemplo com estrutura correta"""
    print("Criando datasets de exemplo...")
    
    # Estrutura base
    columns = [
        'track_name', 'artist_name', 'bpm', 'energy', 'danceability',
        'valence', 'acousticness', 'instrumentalness', 'liveness',
        'speechiness', 'loudness', 'is_hit'
    ]
    
    # Características típicas de cada gênero (baseado nas heurísticas)
    genre_profiles = {
        'sertanejo': {
            'bpm': (120, 140),
            'energy': (0.75, 0.9),
            'danceability': (0.6, 0.8),
            'loudness': (-6.5, -4.5),
            'valence': (0.6, 0.8),
            'acousticness': (0.2, 0.5),
            'sample_size': 20  # Tamanho reduzido para exemplo
        },
        'forro': {
            'bpm': (130, 170),
            'energy': (0.7, 0.95),
            'danceability': (0.6, 0.9),
            'loudness': (-7, -5),
            'valence': (0.7, 0.9),
            'acousticness': (0.3, 0.6),
            'sample_size': 20
        },
        'pagode': {
            'bpm': (90, 125),
            'energy': (0.6, 0.9),
            'danceability': (0.7, 0.95),
            'loudness': (-8, -5),
            'valence': (0.6, 0.85),
            'acousticness': (0.1, 0.4),
            'sample_size': 20
        },
        'samba': {
            'bpm': (90, 125),
            'energy': (0.6, 0.9),
            'danceability': (0.7, 0.95),
            'loudness': (-8, -5),
            'valence': (0.65, 0.9),
            'acousticness': (0.2, 0.5),
            'sample_size': 20
        }
    }
    
    import numpy as np
    np.random.seed(42)
    
    datasets_dir = 'ml/datasets'
    os.makedirs(datasets_dir, exist_ok=True)
    
    for genre, profile in genre_profiles.items():
        print(f"\n  Criando dataset para {genre}...")
        
        data = []
        sample_size = profile['sample_size']
        
        # Cria metade como hits, metade como não-hits
        for i in range(sample_size):
            is_hit = 1 if i < sample_size // 2 else 0
            
            # Gera valores aleatórios dentro dos ranges
            # Hits tendem a estar mais próximos do centro do range
            if is_hit:
                bpm = np.random.normal(np.mean(profile['bpm']), 5)
                energy = np.random.normal(np.mean(profile['energy']), 0.05)
                danceability = np.random.normal(np.mean(profile['danceability']), 0.05)
                valence = np.random.normal(np.mean(profile['valence']), 0.05)
                acousticness = np.random.normal(np.mean(profile['acousticness']), 0.05)
                loudness = np.random.normal(np.mean(profile['loudness']), 0.5)
            else:
                # Não-hits têm mais variação
                bpm = np.random.uniform(*profile['bpm'])
                energy = np.random.uniform(0.3, 1.0)
                danceability = np.random.uniform(0.3, 1.0)
                valence = np.random.uniform(0.2, 1.0)
                acousticness = np.random.uniform(0.0, 0.8)
                loudness = np.random.uniform(-12, -3)
            
            # Outras features com valores padrão
            instrumentalness = np.random.uniform(0.0, 0.1)
            liveness = np.random.uniform(0.1, 0.3)
            speechiness = np.random.uniform(0.03, 0.15)
            
            data.append({
                'track_name': f'{genre.capitalize()} Song {i+1}',
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
        output_file = os.path.join(datasets_dir, f'kaggle_{genre}_ml.csv')
        df.to_csv(output_file, index=False)
        
        print(f"  OK Salvo: {output_file}")
        print(f"    - {len(df)} musicas ({sum(df['is_hit']==1)} hits, {sum(df['is_hit']==0)} nao-hits)")

def main():
    print(INSTRUCTIONS)
    
    # Verifica se há arquivo raw
    raw_file = 'ml/datasets/raw/brazilian_music_raw.csv'
    
    if os.path.exists(raw_file):
        print(f"OK Arquivo encontrado: {raw_file}")
        print("TODO: Implementar processamento do arquivo real")
        print("Por enquanto, criando datasets de exemplo...\n")
    else:
        print("AVISO: Arquivo raw nao encontrado.")
        print("Criando datasets de EXEMPLO com estrutura correta...\n")
    
    create_sample_datasets()
    
    print("\n" + "="*80)
    print("DATASETS DE EXEMPLO CRIADOS!")
    print("="*80)
    print("\nPRÓXIMOS PASSOS:")
    print("1. Estes são apenas exemplos com dados sintéticos")
    print("2. Para dados reais, baixe do Kaggle e coloque em ml/datasets/raw/")
    print("3. Ou substitua manualmente os CSVs com dados reais")
    print("4. Execute: python retrain_models.py")
    print("\n" + "="*80)

if __name__ == "__main__":
    main()
