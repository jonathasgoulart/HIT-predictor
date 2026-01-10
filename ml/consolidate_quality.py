"""
Script melhorado de consolidação que lida melhor com valores faltantes
Estratégia: Usar master datasets como base e adicionar apenas dados completos
"""
import pandas as pd
from pathlib import Path

def consolidate_improved():
    """Consolidação melhorada priorizando qualidade sobre quantidade"""
    datasets_dir = Path(__file__).parent / 'datasets'
    
    print("="*70)
    print("CONSOLIDAÇÃO MELHORADA - PRIORIDADE: QUALIDADE")
    print("="*70 + "\n")
    
    # Estratégia: Começar com master datasets (alta qualidade)
    # e adicionar apenas dados completos de outras fontes
    
    consolidated = {}
    
    # 1. MPB - Começar com master
    print("[1/7] MPB...")
    mpb_sources = []
    
    # Master MPB (base de alta qualidade)
    master_mpb = datasets_dir / 'master_mpb.csv'
    if master_mpb.exists():
        df = pd.read_csv(master_mpb)
        mpb_sources.append(df)
        print(f"  + master_mpb.csv: {len(df)} músicas")
    
    # Kaggle MPB expandido
    kaggle_mpb = datasets_dir / 'kaggle_mpb.csv'
    if kaggle_mpb.exists():
        df = pd.read_csv(kaggle_mpb)
        # Filtrar apenas com dados completos
        required = ['bpm', 'energy', 'danceability', 'loudness']
        df_complete = df.dropna(subset=[c for c in required if c in df.columns])
        if len(df_complete) > 0:
            mpb_sources.append(df_complete)
            print(f"  + kaggle_mpb.csv: {len(df_complete)} músicas completas")
    
    if mpb_sources:
        mpb_combined = pd.concat(mpb_sources, ignore_index=True)
        # Remover duplicatas
        if 'track_name' in mpb_combined.columns and 'artist' in mpb_combined.columns:
            mpb_combined = mpb_combined.drop_duplicates(subset=['track_name', 'artist'])
        consolidated['mpb'] = mpb_combined
        print(f"  -> Total MPB: {len(mpb_combined)} musicas\n")
    
    # 2. R&B Brasil
    print("[2/7] R&B Brasil...")
    rnb_sources = []
    
    master_rnb = datasets_dir / 'master_rnb_brasil.csv'
    if master_rnb.exists():
        df = pd.read_csv(master_rnb)
        rnb_sources.append(df)
        print(f"  + master_rnb_brasil.csv: {len(df)} músicas")
    
    kaggle_rnb = datasets_dir / 'kaggle_rnb_ml.csv'
    if kaggle_rnb.exists():
        df = pd.read_csv(kaggle_rnb)
        rnb_sources.append(df)
        print(f"  + kaggle_rnb_ml.csv: {len(df)} músicas")
    
    if rnb_sources:
        rnb_combined = pd.concat(rnb_sources, ignore_index=True)
        if 'track_name' in rnb_combined.columns:
            rnb_combined = rnb_combined.drop_duplicates(subset=['track_name'])
        consolidated['rnb_brasil'] = rnb_combined
        print(f"  -> Total R&B: {len(rnb_combined)} musicas\n")
    
    # 3-7. Outros gêneros - Usar apenas Kaggle ML (dados limpos)
    kaggle_genres = {
        'sertanejo': 'kaggle_sertanejo_ml.csv',
        'pagode': 'kaggle_pagode_ml.csv',
        'samba': 'kaggle_samba_ml.csv',
        'forro': 'kaggle_forro_ml.csv',
        'pop_urban_brasil': 'kaggle_pop_urban_brasil_ml.csv'
    }
    
    for idx, (genre, filename) in enumerate(kaggle_genres.items(), start=3):
        print(f"[{idx}/7] {genre.upper()}...")
        filepath = datasets_dir / filename
        if filepath.exists():
            df = pd.read_csv(filepath)
            consolidated[genre] = df
            print(f"  + {filename}: {len(df)} musicas\n")
        else:
            print(f"  X {filename} nao encontrado\n")
    
    # Salvar datasets consolidados
    print("="*70)
    print("SALVANDO DATASETS CONSOLIDADOS (QUALIDADE)")
    print("="*70 + "\n")
    
    output_dir = datasets_dir / 'ml_ready'
    output_dir.mkdir(exist_ok=True)
    
    total = 0
    for genre, df in consolidated.items():
        output_file = output_dir / f'{genre}_ml_ready.csv'
        df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"[OK] {genre.upper():<20} {len(df):>5} musicas -> {output_file.name}")
        total += len(df)
    
    print(f"\n{'='*70}")
    print(f"TOTAL: {total} músicas de alta qualidade")
    print(f"{'='*70}\n")
    
    print("Datasets salvos em: ml/datasets/ml_ready/")
    print("\nPróximo passo:")
    print("  python ml/train_master_models.py")
    
    return consolidated

if __name__ == "__main__":
    consolidate_improved()
