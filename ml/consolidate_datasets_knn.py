"""
Versão otimizada da consolidação de datasets
Usa KNN Imputation para recuperar músicas com valores faltantes
"""
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.impute import KNNImputer

def load_available_datasets():
    """Carrega todos os datasets disponíveis"""
    datasets_dir = Path(__file__).parent / 'datasets'
    
    all_datasets = {
        'mpb': [],
        'rnb_brasil': [],
        'sertanejo': [],
        'pagode': [],
        'samba': [],
        'forro': [],
        'pop_urban_brasil': []
    }
    
    print("="*70)
    print("CONSOLIDACAO DE DATASETS COM KNN IMPUTATION")
    print("="*70 + "\n")
    
    # 1. Massive Brazil Spotify
    massive_file = datasets_dir / 'massive_brazil_spotify.csv'
    if massive_file.exists():
        print(f"[1/6] Carregando {massive_file.name}...")
        try:
            df_massive = pd.read_csv(massive_file)
            print(f"      Total: {len(df_massive)} musicas")
            
            genre_col = 'track_genre' if 'track_genre' in df_massive.columns else 'genre'
            
            if genre_col in df_massive.columns:
                genre_mapping = {
                    'mpb': ['mpb'],
                    'pagode': ['pagode'],
                    'samba': ['samba'],
                    'forro': ['forro', 'forro'],
                    'sertanejo': ['sertanejo'],
                    'pop_urban_brasil': ['brazil', 'pop', 'funk'],
                    'rnb_brasil': ['rnb', 'r&b', 'r-n-b']
                }
                
                for target_genre, source_genres in genre_mapping.items():
                    genre_data = df_massive[df_massive[genre_col].str.lower().isin([g.lower() for g in source_genres])]
                    if len(genre_data) > 0:
                        all_datasets[target_genre].append(genre_data.copy())
                        print(f"      + {target_genre}: {len(genre_data)} musicas")
        except Exception as e:
            print(f"      X Erro: {e}")
    
    # 2. Spotify 114k
    print(f"\n[2/6] Verificando Spotify 114k...")
    spotify_114k = datasets_dir / 'spotify_114k' / 'dataset.csv'
    if spotify_114k.exists():
        print(f"      Carregando {spotify_114k.name}...")
        try:
            df_114k = pd.read_csv(spotify_114k)
            print(f"      Total: {len(df_114k)} musicas")
            
            genre_col = 'track_genre' if 'track_genre' in df_114k.columns else 'genre'
            if genre_col in df_114k.columns:
                brazilian_genres = ['mpb', 'pagode', 'samba', 'forro', 'sertanejo', 'brazil', 'bossanova']
                df_brazil = df_114k[df_114k[genre_col].str.lower().isin(brazilian_genres)]
                
                for genre in all_datasets.keys():
                    if genre == 'pop_urban_brasil':
                        genre_filter = ['brazil', 'bossanova']
                    else:
                        genre_filter = [genre]
                    
                    genre_data = df_brazil[df_brazil[genre_col].str.lower().isin(genre_filter)]
                    if len(genre_data) > 0:
                        all_datasets[genre].append(genre_data.copy())
                        print(f"      + {genre}: {len(genre_data)} musicas")
        except Exception as e:
            print(f"      X Erro: {e}")
    
    # 3. Master Datasets
    print(f"\n[3/6] Carregando master datasets...")
    master_files = {
        'mpb': datasets_dir / 'master_mpb.csv',
        'rnb_brasil': datasets_dir / 'master_rnb_brasil.csv'
    }
    
    for genre, filepath in master_files.items():
        if filepath.exists():
            try:
                df = pd.read_csv(filepath)
                all_datasets[genre].append(df.copy())
                print(f"      + {genre}: {len(df)} musicas")
            except Exception as e:
                print(f"      X Erro em {filepath.name}: {e}")
    
    # 4. Kaggle ML datasets
    print(f"\n[4/6] Carregando Kaggle ML datasets...")
    kaggle_ml_files = {
        'mpb': 'kaggle_mpb_ml.csv',
        'sertanejo': 'kaggle_sertanejo_ml.csv',
        'pagode': 'kaggle_pagode_ml.csv',
        'samba': 'kaggle_samba_ml.csv',
        'forro': 'kaggle_forro_ml.csv',
        'pop_urban_brasil': 'kaggle_pop_urban_brasil_ml.csv'
    }
    
    for genre, filename in kaggle_ml_files.items():
        filepath = datasets_dir / filename
        if filepath.exists():
            try:
                df = pd.read_csv(filepath)
                all_datasets[genre].append(df.copy())
                print(f"      + {genre}: {len(df)} musicas")
            except Exception as e:
                print(f"      X Erro em {filename}: {e}")
    
    # 5. Datasets individuais
    print(f"\n[5/6] Carregando datasets individuais...")
    individual_files = {
        'mpb': 'mpb_dataset.csv',
        'rnb_brasil': 'rnb_brasil_dataset.csv'
    }
    
    for genre, filename in individual_files.items():
        filepath = datasets_dir / filename
        if filepath.exists():
            try:
                df = pd.read_csv(filepath)
                all_datasets[genre].append(df.copy())
                print(f"      + {genre}: {len(df)} musicas")
            except Exception as e:
                print(f"      X Erro em {filename}: {e}")
    
    # 6. Kaggle Brazilian Music
    print(f"\n[6/6] Carregando Kaggle Brazilian Music...")
    kaggle_file = datasets_dir / 'kaggle_brazilian_music.csv'
    if kaggle_file.exists():
        try:
            df_kaggle = pd.read_csv(kaggle_file)
            print(f"      Total: {len(df_kaggle)} musicas")
        except Exception as e:
            print(f"      X Erro: {e}")
    
    return all_datasets

def merge_and_deduplicate(datasets_dict):
    """Consolida e remove duplicatas"""
    print("\n" + "="*70)
    print("CONSOLIDACAO E REMOCAO DE DUPLICATAS")
    print("="*70 + "\n")
    
    consolidated = {}
    
    for genre, df_list in datasets_dict.items():
        if not df_list:
            print(f"{genre.upper()}: Nenhum dataset encontrado")
            continue
        
        df_combined = pd.concat(df_list, ignore_index=True)
        before_dedup = len(df_combined)
        print(f"{genre.upper()}: {before_dedup} musicas (antes de deduplicacao)")
        
        # Identifica colunas de identificação
        id_cols = []
        if 'track_name' in df_combined.columns:
            id_cols.append('track_name')
        if 'artist' in df_combined.columns:
            id_cols.append('artist')
        elif 'artist_name' in df_combined.columns:
            id_cols.append('artist_name')
        elif 'artists' in df_combined.columns:
            id_cols.append('artists')
        
        # Remove duplicatas
        if id_cols:
            df_combined = df_combined.drop_duplicates(subset=id_cols, keep='first')
            removed = before_dedup - len(df_combined)
            print(f"          + Removidas {removed} duplicatas ({removed/before_dedup*100:.1f}%)")
        
        consolidated[genre] = df_combined
    
    return consolidated

def apply_knn_imputation(df, genre_name):
    """Aplica KNN Imputation para preencher valores faltantes"""
    print(f"\n  [KNN] Processando {genre_name}...")
    
    # Features críticas para ML
    critical_features = ['bpm', 'energy', 'danceability', 'valence', 
                        'acousticness', 'instrumentalness', 'liveness', 
                        'speechiness', 'loudness']
    
    # Verifica quais features existem
    available_features = [f for f in critical_features if f in df.columns]
    
    if not available_features:
        print(f"        Nenhuma feature critica encontrada")
        return df
    
    before_imputation = len(df)
    
    # Remove linhas completamente vazias (todas features faltando)
    df_clean = df.dropna(subset=available_features, how='all')
    
    # Conta valores faltantes antes
    missing_before = df_clean[available_features].isnull().sum().sum()
    print(f"        Valores faltantes: {missing_before}")
    
    if missing_before == 0:
        print(f"        Nenhum valor para imputar OK")
        return df_clean
    
    # Aplica KNN Imputation
    try:
        imputer = KNNImputer(n_neighbors=5, weights='distance')
        
        # Imputa apenas as features disponíveis
        df_imputed = df_clean.copy()
        df_imputed[available_features] = imputer.fit_transform(df_clean[available_features])
        
        # Conta valores faltantes depois
        missing_after = df_imputed[available_features].isnull().sum().sum()
        recovered = missing_before - missing_after
        
        print(f"        Valores preenchidos: {recovered}")
        print(f"        Musicas recuperadas: {before_imputation - len(df_clean)} -> 0")
        
        return df_imputed
        
    except Exception as e:
        print(f"        X Erro no KNN: {e}")
        print(f"        Usando dataset sem imputacao")
        return df_clean

def save_consolidated_datasets(consolidated_dict):
    """Salva datasets consolidados"""
    print("\n" + "="*70)
    print("SALVANDO DATASETS CONSOLIDADOS")
    print("="*70 + "\n")
    
    output_dir = Path(__file__).parent / 'datasets' / 'consolidated_knn'
    output_dir.mkdir(exist_ok=True)
    
    summary = []
    
    for genre, df in consolidated_dict.items():
        output_file = output_dir / f'{genre}_consolidated.csv'
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"[OK] {genre.upper():<20} {len(df):>5} musicas -> {output_file.name}")
        summary.append((genre, len(df)))
    
    # Cria relatório
    report = []
    report.append("# Relatorio de Consolidacao com KNN Imputation\n")
    report.append(f"Data: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    report.append("## Metodo\n")
    report.append("- KNN Imputation (k=5) para preencher valores faltantes")
    report.append("- Features imputadas: bpm, energy, danceability, valence, etc.\n")
    report.append("## Resumo\n")
    report.append("| Genero | Musicas | Arquivo |")
    report.append("|--------|---------|---------|")
    for genre, count in summary:
        report.append(f"| {genre} | {count} | {genre}_consolidated.csv |")
    
    report.append("\n## Proximos Passos\n")
    report.append("1. Retreinar modelos com datasets expandidos:")
    report.append("   ```bash")
    report.append("   python ml/train_all_models.py --use-consolidated-knn")
    report.append("   ```")
    
    report_file = output_dir / 'README.md'
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))
    
    print(f"\n[OK] Relatorio salvo: {report_file}")

def print_summary(consolidated_dict):
    """Imprime resumo estatístico"""
    print("\n" + "="*70)
    print("RESUMO FINAL")
    print("="*70 + "\n")
    
    total_tracks = sum(len(df) for df in consolidated_dict.values())
    print(f"Total de musicas consolidadas: {total_tracks}\n")
    
    for genre, df in sorted(consolidated_dict.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"{genre.upper():<20} {len(df):>5} musicas")

def main():
    # Carrega datasets
    all_datasets = load_available_datasets()
    
    # Consolida e remove duplicatas
    consolidated = merge_and_deduplicate(all_datasets)
    
    # Aplica KNN Imputation
    print("\n" + "="*70)
    print("APLICANDO KNN IMPUTATION")
    print("="*70)
    
    consolidated_knn = {}
    for genre, df in consolidated.items():
        df_imputed = apply_knn_imputation(df, genre)
        consolidated_knn[genre] = df_imputed
    
    # Salva
    save_consolidated_datasets(consolidated_knn)
    
    # Resumo
    print_summary(consolidated_knn)
    
    print("\n" + "="*70)
    print("OK CONSOLIDACAO COM KNN CONCLUIDA!")
    print("="*70)
    print("\nDatasets estao em: ml/datasets/consolidated_knn/")
    print("\nProximo passo:")
    print("  python ml/train_all_models.py --use-consolidated-knn")

if __name__ == "__main__":
    main()
