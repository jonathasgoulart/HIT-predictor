"""
Processa dados reais do Spotify (30k músicas) e extrai gêneros brasileiros
"""
import pandas as pd
import numpy as np
import os
import sys

# Corrige problema de encoding no terminal Windows
sys.stdout.reconfigure(encoding='utf-8')

def process_data():
    file_path = 'ml/datasets/raw/spotify_songs.csv'
    raw_dir = 'ml/datasets/raw'
    out_dir = 'ml/datasets'
    
    print(f"Carregando {file_path}...")
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        df = pd.read_csv(file_path, encoding='latin1')
        
    print(f"Total de musicas: {len(df)}")
    
    # Critérios de filtragem para cada gênero
    # Procuramos nos campos: playlist_name, playlist_genre, playlist_subgenre
    
    # Dicionário de artistas/termos para filtrar do dataset 'latin'
    keywords_map = {
        'sertanejo': ['sertanejo', 'marilia mendonca', 'gusttavo lima', 'jorge & mateus', 'henrique & juliano', 'matheus & kauan', 'maiara & maraisa', 'simone & simaria', 'luan santana', 'ze neto & cristiano'],
        'forro': ['forro', 'piseiro', 'wesley safadao', 'xand aviao', 'joao gomes', 'nattan', 'tarcisio do acordeon', 'baroes da pisadinha', 'calcinha preta'],
        'pagode': ['pagode', 'thiaguinho', 'sorriso maroto', 'dilsinho', 'menons at work', 'ferrugem', 'mumuzinho', 'pixote', 'turma do pagode', 'exaltasamba'],
        'samba': ['samba', 'zeca pagodinho', 'martinho da vila', 'alcione', 'jorge aragao', 'diogo nogueira', 'beth carvalho', 'fundo de quintal'],
        'pop_urban_brasil': ['funk', 'anitta', 'ludmilla', 'pabllo vittar', 'luis sonsa', 'pedro sampaio', 'kevinho', 'mc', 'hungria', 'matue', 'filipe ret', 'l7nnon', 'gloria groove', 'iza'],
        'mpb': ['mpb', 'caetano veloso', 'gilberto gil', 'chico buarque', 'gal costa', 'maria bethania', 'djavan', 'milton nascimento', 'elis regina', 'alceu valenca']
    }
    
    # Processa dataset Latin para extrair brasileiros
    print("\nProcessando sub-generos brasileiros dentro de 'latin'...")
    latin_mask = df['playlist_genre'] == 'latin'
    latin_df = df[latin_mask].copy()
    
    genres = {}
    
    for genre_id, terms in keywords_map.items():
        # Busca termos no nome da playlist, nome da musica ou nome do artista
        mask = pd.Series([False] * len(latin_df))
        
        for term in terms:
            term = term.lower()
            m1 = latin_df['playlist_name'].str.lower().str.contains(term, na=False)
            m2 = latin_df['track_name'].str.lower().str.contains(term, na=False)
            m3 = latin_df['track_artist'].str.lower().str.contains(term, na=False)
            m4 = latin_df['playlist_subgenre'].str.lower().str.contains(term, na=False)
            mask = mask | m1 | m2 | m3 | m4
            
        genre_df = latin_df[mask].copy()
        
        # Se encontrou poucas, tenta buscar no dataset inteiro (não só latin)
        if len(genre_df) < 20:
             mask_all = pd.Series([False] * len(df))
             for term in terms:
                term = term.lower()
                m1 = df['playlist_name'].str.lower().str.contains(term, na=False)
                m2 = df['track_name'].str.lower().str.contains(term, na=False)
                m3 = df['track_artist'].str.lower().str.contains(term, na=False)
                mask_all = mask_all | m1 | m2 | m3
             genre_df = df[mask_all].copy()
        
        genres[genre_id] = genre_df.drop_duplicates(subset=['track_name', 'track_artist'])
        
    created_files = []
    final_cols = [
        'track_name', 'artist_name', 'bpm', 'energy', 'danceability',
        'valence', 'acousticness', 'instrumentalness', 'liveness',
        'speechiness', 'loudness', 'is_hit'
    ]

    for genre_id, genre_df in genres.items():
        print(f"\nProcessando {genre_id}...")
        
        if len(genre_df) == 0:
            print(f"  AVISO: Nenhuma musica encontrada para {genre_id}")
            continue
            
        print(f"  Encontradas: {len(genre_df)} musicas")
        
        # Mapeia colunas para nosso formato
        genre_df['artist_name'] = genre_df['track_artist']
        genre_df['bpm'] = genre_df['tempo']
        
        # Cria label 'is_hit' baseado em popularidade
        # Top 50% = hit (1), Bottom 50% = não-hit (0)
        median_pop = genre_df['track_popularity'].median()
        genre_df['is_hit'] = (genre_df['track_popularity'] >= median_pop).astype(int)
        
        # Seleciona apenas colunas necessárias
        final_df = genre_df[final_cols].copy()
        
        # Remove duplicatas (mesma música pode estar em várias playlists)
        final_df = final_df.drop_duplicates(subset=['track_name', 'artist_name'])
        
        # Salva arquivo
        out_file = os.path.join(out_dir, f'kaggle_{genre_id}_ml.csv')
        final_df.to_csv(out_file, index=False)
        print(f"  Salvo: {out_file} ({len(final_df)} unicas)")
        
        created_files.append(genre_id)
        
    return created_files

if __name__ == "__main__":
    process_data()
