"""
Análise de Notas por Assinatura Sonora - 10 Músicas da Base de Dados
"""
import pandas as pd
import os

print("="*80)
print("ANÁLISE DE SCORES - 10 MÚSICAS DA BASE DE DADOS")
print("="*80)

# Carrega o dataset principal
dataset_path = os.path.join('ml', 'datasets', 'master_mpb.csv')

if not os.path.exists(dataset_path):
    # Tenta outro dataset
    dataset_path = os.path.join('ml', 'datasets', 'mpb_dataset.csv')

if not os.path.exists(dataset_path):
    print(f"\n❌ Dataset não encontrado!")
    print("Procurando datasets disponíveis...")
    
    datasets_dir = os.path.join('ml', 'datasets')
    csv_files = [f for f in os.listdir(datasets_dir) if f.endswith('.csv') and 'regional' not in f]
    
    if csv_files:
        dataset_path = os.path.join(datasets_dir, csv_files[0])
        print(f"✓ Usando: {csv_files[0]}")
    else:
        print("Nenhum dataset CSV encontrado!")
        exit(1)

# Carrega dados
print(f"\n[1] Carregando dataset: {os.path.basename(dataset_path)}")
df = pd.read_csv(dataset_path)

print(f"    Total de músicas: {len(df)}")
print(f"    Colunas: {list(df.columns)}")

# Seleciona 10 músicas variadas (5 hits + 5 não-hits se possível)
print(f"\n[2] Selecionando 10 músicas para análise...")

if 'is_hit' in df.columns:
    # Pega 5 hits e 5 não-hits
    hits = df[df['is_hit'] == 1].head(5)
    non_hits = df[df['is_hit'] == 0].head(5)
    sample = pd.concat([hits, non_hits])
else:
    # Pega 10 músicas aleatórias
    sample = df.sample(n=min(10, len(df)), random_state=42)

print(f"    Músicas selecionadas: {len(sample)}")

# Identifica features de áudio relevantes
audio_features = ['bpm', 'energy', 'danceability', 'valence', 'acousticness', 
                  'instrumentalness', 'liveness', 'speechiness', 'loudness']

available_features = [f for f in audio_features if f in df.columns]

print(f"\n[3] Features de áudio disponíveis: {len(available_features)}")
print(f"    {', '.join(available_features)}")

# Exibe análise detalhada
print(f"\n{'='*80}")
print("ANÁLISE DETALHADA DAS 10 MÚSICAS")
print(f"{'='*80}\n")

for idx, (i, row) in enumerate(sample.iterrows(), 1):
    print(f"{'-'*80}")
    print(f"MUSICA #{idx}")
    print(f"{'-'*80}")
    
    # Informações básicas
    if 'track_name' in row:
        print(f"Nome: {row['track_name']}")
    if 'artist' in row:
        print(f"Artista: {row['artist']}")
    if 'is_hit' in row:
        status = "[HIT]" if row['is_hit'] == 1 else "[NAO-HIT]"
        print(f"Status: {status}")
    if 'popularity' in row:
        print(f"Popularidade: {row['popularity']}")
    
    print(f"\nASSINATURA SONORA (Features de Audio):")
    print(f"{'-'*80}")
    
    # Exibe cada feature com barra visual
    for feature in available_features:
        if feature in row and pd.notna(row[feature]):
            value = row[feature]
            
            # Normaliza valor para barra visual (0-100)
            if feature == 'loudness':
                # Loudness geralmente é negativo (-60 a 0)
                normalized = max(0, min(100, (value + 60) * 100 / 60))
            elif feature == 'bpm':
                # BPM geralmente 60-180
                normalized = max(0, min(100, (value - 60) * 100 / 120))
            else:
                # Outros features geralmente 0-1
                normalized = value * 100 if value <= 1 else min(100, value)
            
            # Cria barra visual
            bar_length = int(normalized / 2)  # 50 caracteres max
            bar = '#' * bar_length + '.' * (50 - bar_length)
            
            # Formata valor
            if feature == 'loudness':
                value_str = f"{value:.1f} dB"
            elif feature == 'bpm':
                value_str = f"{value:.0f} BPM"
            else:
                value_str = f"{value:.3f}"
            
            print(f"  {feature:20s} {bar} {value_str:>12s}")
    
    print()

# Estatísticas gerais
print(f"\n{'='*80}")
print("ESTATISTICAS GERAIS DA AMOSTRA")
print(f"{'='*80}\n")

for feature in available_features:
    if feature in sample.columns:
        values = sample[feature].dropna()
        if len(values) > 0:
            print(f"{feature:20s} | Media: {values.mean():8.2f} | Min: {values.min():8.2f} | Max: {values.max():8.2f}")

# Comparação Hits vs Não-Hits (se disponível)
if 'is_hit' in sample.columns:
    print(f"\n{'='*80}")
    print("COMPARACAO: HITS vs NAO-HITS")
    print(f"{'='*80}\n")
    
    hits = sample[sample['is_hit'] == 1]
    non_hits = sample[sample['is_hit'] == 0]
    
    print(f"{'Feature':20s} | {'Hits (Media)':>15s} | {'Nao-Hits (Media)':>18s} | {'Diferenca':>12s}")
    print(f"{'-'*80}")
    
    for feature in available_features:
        if feature in sample.columns:
            hit_mean = hits[feature].mean()
            non_hit_mean = non_hits[feature].mean()
            diff = hit_mean - non_hit_mean
            
            if pd.notna(hit_mean) and pd.notna(non_hit_mean):
                print(f"{feature:20s} | {hit_mean:15.3f} | {non_hit_mean:18.3f} | {diff:+12.3f}")

print(f"\n{'='*80}")
print("ANÁLISE CONCLUÍDA")
print(f"{'='*80}\n")
