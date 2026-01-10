"""
Quick Win #1: Validar e Limpar Datasets
Remove duplicatas, outliers e valida distribuição de hits/non-hits
"""
import pandas as pd
import numpy as np
import os
from pathlib import Path

def validate_dataset(csv_path):
    """Valida dataset e retorna lista de issues"""
    print(f"\n{'='*70}")
    print(f"VALIDANDO: {os.path.basename(csv_path)}")
    print(f"{'='*70}\n")
    
    if not os.path.exists(csv_path):
        return [f"Arquivo não encontrado: {csv_path}"]
    
    df = pd.read_csv(csv_path)
    issues = []
    stats = {}
    
    # 1. Info básica
    stats['total_rows'] = len(df)
    stats['total_columns'] = len(df.columns)
    print(f"Total de músicas: {len(df)}")
    print(f"Colunas: {len(df.columns)}")
    
    # 2. Detectar duplicatas
    # Tenta usar track_name + artist, se não tiver artist usa só track_name
    dup_cols = []
    if 'track_name' in df.columns:
        dup_cols.append('track_name')
    if 'artist' in df.columns:
        dup_cols.append('artist')
    
    if dup_cols:
        duplicates = df[df.duplicated(subset=dup_cols, keep=False)]
        if len(duplicates) > 0:
            issues.append(f"AVISO: Duplicatas encontradas: {len(duplicates)} musicas")
            stats['duplicates'] = len(duplicates)
            print(f"AVISO: Duplicatas: {len(duplicates)}")
        else:
            print("OK: Sem duplicatas")
            stats['duplicates'] = 0
    else:
        print("AVISO: Nao foi possivel verificar duplicatas (colunas nao encontradas)")
        stats['duplicates'] = 0
    
    # 3. Verificar distribuição hits/non-hits
    if 'is_hit' in df.columns:
        hit_ratio = df['is_hit'].mean()
        stats['hit_ratio'] = hit_ratio
        print(f"Distribuição: {hit_ratio:.1%} hits, {1-hit_ratio:.1%} non-hits")
        
        if hit_ratio < 0.2 or hit_ratio > 0.8:
            issues.append(f"AVISO:  Distribuição muito desbalanceada: {hit_ratio:.1%} hits")
        else:
            print("OK: Distribuição balanceada")
    
    # 4. Detectar outliers em features numéricas
    numeric_cols = ['bpm', 'energy', 'danceability', 'loudness', 'valence']
    outlier_counts = {}
    
    for col in numeric_cols:
        if col in df.columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            
            # Outliers extremos (3 IQR)
            outliers = df[(df[col] < Q1 - 3*IQR) | (df[col] > Q3 + 3*IQR)]
            outlier_counts[col] = len(outliers)
            
            if len(outliers) > 0:
                pct = len(outliers) / len(df) * 100
                print(f"AVISO:  Outliers em {col}: {len(outliers)} ({pct:.1f}%)")
                if pct > 5:
                    issues.append(f"AVISO:  Muitos outliers em {col}: {pct:.1f}%")
    
    stats['outliers'] = outlier_counts
    
    # 5. Valores faltantes
    missing = df.isnull().sum()
    if missing.sum() > 0:
        print(f"\nAVISO:  Valores faltantes:")
        for col, count in missing[missing > 0].items():
            pct = count / len(df) * 100
            print(f"   {col}: {count} ({pct:.1f}%)")
            if pct > 10:
                issues.append(f"AVISO:  Muitos valores faltantes em {col}: {pct:.1f}%")
    else:
        print("OK: Sem valores faltantes")
    
    stats['missing'] = missing.to_dict()
    
    print(f"\n{'='*70}")
    print(f"RESUMO: {len(issues)} issues encontrados")
    print(f"{'='*70}\n")
    
    return issues, stats

def clean_dataset(csv_path, output_path=None):
    """Limpa dataset removendo duplicatas e outliers"""
    print(f"\n{'='*70}")
    print(f"LIMPANDO: {os.path.basename(csv_path)}")
    print(f"{'='*70}\n")
    
    df = pd.read_csv(csv_path)
    original_size = len(df)
    
    # 1. Remove duplicatas
    dup_cols = []
    if 'track_name' in df.columns:
        dup_cols.append('track_name')
    if 'artist' in df.columns:
        dup_cols.append('artist')
    
    if dup_cols:
        df_clean = df.drop_duplicates(subset=dup_cols, keep='first')
        removed_dupes = original_size - len(df_clean)
        if removed_dupes > 0:
            print(f"OK: Removidas {removed_dupes} duplicatas")
    else:
        df_clean = df.copy()
        removed_dupes = 0
    
    # 2. Remove outliers extremos (3 IQR)
    numeric_cols = ['bpm', 'energy', 'danceability', 'loudness', 'valence']
    removed_outliers = 0
    
    for col in numeric_cols:
        if col in df_clean.columns:
            before = len(df_clean)
            Q1 = df_clean[col].quantile(0.25)
            Q3 = df_clean[col].quantile(0.75)
            IQR = Q3 - Q1
            
            df_clean = df_clean[
                (df_clean[col] >= Q1 - 3*IQR) & 
                (df_clean[col] <= Q3 + 3*IQR)
            ]
            
            removed = before - len(df_clean)
            if removed > 0:
                removed_outliers += removed
                print(f"OK: Removidos {removed} outliers de {col}")
    
    # 3. Remove linhas com valores faltantes críticos
    critical_cols = ['bpm', 'energy', 'danceability', 'is_hit']
    before = len(df_clean)
    df_clean = df_clean.dropna(subset=[c for c in critical_cols if c in df_clean.columns])
    removed_na = before - len(df_clean)
    if removed_na > 0:
        print(f"OK: Removidas {removed_na} linhas com valores faltantes")
    
    # 4. Salva dataset limpo
    if output_path is None:
        output_path = csv_path.replace('.csv', '_clean.csv')
    
    df_clean.to_csv(output_path, index=False)
    
    final_size = len(df_clean)
    total_removed = original_size - final_size
    pct_removed = total_removed / original_size * 100
    
    print(f"\n{'='*70}")
    print(f"RESULTADO:")
    print(f"  Original: {original_size} músicas")
    print(f"  Limpo: {final_size} músicas")
    print(f"  Removido: {total_removed} ({pct_removed:.1f}%)")
    print(f"  Salvo em: {output_path}")
    print(f"{'='*70}\n")
    
    return df_clean, output_path

def main():
    """Valida e limpa todos os datasets"""
    datasets_dir = Path(__file__).parent / 'datasets'
    
    datasets = {
        'MPB': 'kaggle_mpb_ml.csv',
        'R&B Brasil': 'kaggle_rnb_ml.csv',
        'Pop Urban': 'kaggle_pop_urban_brasil_ml.csv',
        'Sertanejo': 'kaggle_sertanejo_ml.csv',
        'Pagode': 'kaggle_pagode_ml.csv',
        'Samba': 'kaggle_samba_ml.csv',
        'Forró': 'kaggle_forro_ml.csv'
    }
    
    all_issues = {}
    all_stats = {}
    cleaned_files = {}
    
    print("\n" + "="*70)
    print("VALIDAÇÃO E LIMPEZA DE DATASETS")
    print("="*70)
    
    # Fase 1: Validação
    print("\n[FASE 1: VALIDACAO]\n")
    for genre, filename in datasets.items():
        filepath = datasets_dir / filename
        if filepath.exists():
            issues, stats = validate_dataset(str(filepath))
            all_issues[genre] = issues
            all_stats[genre] = stats
        else:
            print(f"AVISO: {genre}: Arquivo nao encontrado")
    
    # Fase 2: Limpeza
    print("\n[FASE 2: LIMPEZA]\n")
    for genre, filename in datasets.items():
        filepath = datasets_dir / filename
        if filepath.exists() and len(all_issues.get(genre, [])) > 0:
            df_clean, output_path = clean_dataset(str(filepath))
            cleaned_files[genre] = output_path
        else:
            print(f"OK: {genre}: Nenhuma limpeza necessária")
    
    # Relatório Final
    print("\n" + "="*70)
    print("RELATÓRIO FINAL")
    print("="*70 + "\n")
    
    for genre in datasets.keys():
        if genre in all_stats:
            stats = all_stats[genre]
            print(f"{genre}:")
            print(f"  Total: {stats['total_rows']} músicas")
            print(f"  Duplicatas: {stats.get('duplicates', 0)}")
            print(f"  Hit ratio: {stats.get('hit_ratio', 0):.1%}")
            if genre in cleaned_files:
                print(f"  OK: Limpo: {cleaned_files[genre]}")
            print()
    
    print("="*70)
    print("OK: VALIDAÇÃO E LIMPEZA CONCLUÍDA!")
    print("="*70)
    
    return cleaned_files

if __name__ == "__main__":
    main()
