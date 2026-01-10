"""
Passo 1: Validacao Manual de Labels
Analisa e identifica problemas nos labels dos datasets
"""
import pandas as pd
import numpy as np
from pathlib import Path

def analyze_label_distribution(df, genre):
    """Analisa distribuicao de labels e identifica problemas"""
    print(f"\n{'='*70}")
    print(f"ANALISE DE LABELS - {genre.upper()}")
    print(f"{'='*70}\n")
    
    # Distribuicao basica
    total = len(df)
    hits = df['is_hit'].sum()
    non_hits = total - hits
    
    print(f"Total: {total} musicas")
    print(f"Hits: {hits} ({hits/total*100:.1f}%)")
    print(f"Nao-hits: {non_hits} ({non_hits/total*100:.1f}%)")
    
    # Distribuicao de popularidade
    if 'popularity' in df.columns:
        print(f"\nDistribuicao de Popularidade:")
        print(f"  Min: {df['popularity'].min():.0f}")
        print(f"  Max: {df['popularity'].max():.0f}")
        print(f"  Media: {df['popularity'].mean():.1f}")
        print(f"  Mediana: {df['popularity'].median():.1f}")
        
        # Zona cinza (65-75)
        gray_zone = df[(df['popularity'] >= 65) & (df['popularity'] <= 75)]
        print(f"\nZona Cinza (popularity 65-75): {len(gray_zone)} musicas ({len(gray_zone)/total*100:.1f}%)")
        
        # Hits com baixa popularidade
        low_pop_hits = df[(df['is_hit'] == 1) & (df['popularity'] < 70)]
        print(f"Hits com popularity < 70: {len(low_pop_hits)} ({len(low_pop_hits)/hits*100:.1f}% dos hits)")
        
        # Nao-hits com alta popularidade
        high_pop_nonhits = df[(df['is_hit'] == 0) & (df['popularity'] > 70)]
        print(f"Nao-hits com popularity > 70: {len(high_pop_nonhits)} ({len(high_pop_nonhits)/non_hits*100:.1f}% dos nao-hits)")
    
    return {
        'total': total,
        'hits': hits,
        'gray_zone': len(gray_zone) if 'popularity' in df.columns else 0,
        'inconsistent_hits': len(low_pop_hits) if 'popularity' in df.columns else 0,
        'inconsistent_nonhits': len(high_pop_nonhits) if 'popularity' in df.columns else 0
    }

def sample_for_review(df, n=20):
    """Seleciona amostras para revisao manual"""
    print(f"\n{'='*70}")
    print(f"AMOSTRAS PARA REVISAO MANUAL")
    print(f"{'='*70}\n")
    
    samples = []
    
    # 1. Zona cinza
    if 'popularity' in df.columns:
        gray = df[(df['popularity'] >= 65) & (df['popularity'] <= 75)].sample(min(5, len(df)))
        samples.append(('Zona Cinza (65-75)', gray))
    
    # 2. Hits com baixa popularidade
    if 'popularity' in df.columns:
        low_hits = df[(df['is_hit'] == 1) & (df['popularity'] < 70)].sample(min(5, len(df)))
        samples.append(('Hits com Pop < 70', low_hits))
    
    # 3. Nao-hits com alta popularidade
    if 'popularity' in df.columns:
        high_nonhits = df[(df['is_hit'] == 0) & (df['popularity'] > 70)].sample(min(5, len(df)))
        samples.append(('Nao-hits com Pop > 70', high_nonhits))
    
    # 4. Aleatorias
    random = df.sample(min(5, len(df)))
    samples.append(('Aleatorias', random))
    
    # Exibe amostras
    for category, sample_df in samples:
        print(f"\n{category}:")
        print("-" * 70)
        for idx, row in sample_df.iterrows():
            track = row.get('track_name', row.get('name', 'Unknown'))
            artist = row.get('artist', row.get('artist_name', 'Unknown'))
            pop = row.get('popularity', 'N/A')
            label = 'HIT' if row['is_hit'] == 1 else 'NAO-HIT'
            
            print(f"  [{label}] {track} - {artist}")
            print(f"         Popularity: {pop}")
    
    print(f"\n{'='*70}")
    print("REVISAO MANUAL NECESSARIA")
    print(f"{'='*70}")
    print("\nPara cada musica acima, verifique:")
    print("1. A musica realmente e um hit?")
    print("2. O label esta correto?")
    print("3. A popularidade reflete o sucesso real?")

def clean_dataset(df, genre):
    """Limpa dataset removendo zona cinza e inconsistencias"""
    print(f"\n{'='*70}")
    print(f"LIMPEZA DE DATASET - {genre.upper()}")
    print(f"{'='*70}\n")
    
    original_size = len(df)
    
    # 1. Remove zona cinza (popularity 65-75)
    if 'popularity' in df.columns:
        df_clean = df[
            (df['popularity'] < 65) | 
            (df['popularity'] > 75)
        ].copy()
        removed_gray = original_size - len(df_clean)
        print(f"Removidas {removed_gray} musicas da zona cinza (65-75)")
    else:
        df_clean = df.copy()
    
    # 2. Aplica criterio mais rigoroso para hits
    if 'popularity' in df_clean.columns:
        # Hits devem ter popularity > 75 (mais rigoroso)
        df_clean['is_hit_strict'] = (df_clean['popularity'] > 75).astype(int)
        
        # Compara com label original
        changed = (df_clean['is_hit'] != df_clean['is_hit_strict']).sum()
        print(f"Labels que mudariam com criterio rigoroso: {changed}")
        
        # Atualiza labels
        df_clean['is_hit'] = df_clean['is_hit_strict']
        df_clean = df_clean.drop(columns=['is_hit_strict'])
    
    print(f"\nDataset original: {original_size} musicas")
    print(f"Dataset limpo: {len(df_clean)} musicas")
    print(f"Reducao: {original_size - len(df_clean)} musicas ({(original_size - len(df_clean))/original_size*100:.1f}%)")
    
    # Nova distribuicao
    hits_clean = df_clean['is_hit'].sum()
    print(f"\nNova distribuicao:")
    print(f"  Hits: {hits_clean} ({hits_clean/len(df_clean)*100:.1f}%)")
    print(f"  Nao-hits: {len(df_clean) - hits_clean} ({(len(df_clean) - hits_clean)/len(df_clean)*100:.1f}%)")
    
    return df_clean

def main():
    ml_ready_dir = Path(__file__).parent / 'datasets' / 'ml_ready'
    
    datasets = {
        'mpb': ml_ready_dir / 'mpb_ml_ready.csv',
        'rnb_brasil': ml_ready_dir / 'rnb_brasil_ml_ready.csv'
    }
    
    print("="*70)
    print("VALIDACAO E LIMPEZA DE LABELS")
    print("="*70)
    
    for genre, filepath in datasets.items():
        if not filepath.exists():
            print(f"\nArquivo nao encontrado: {filepath}")
            continue
        
        # Carrega dataset
        df = pd.read_csv(filepath)
        
        # Analisa
        stats = analyze_label_distribution(df, genre)
        
        # Amostras para revisao
        sample_for_review(df)
        
        # Limpa dataset
        df_clean = clean_dataset(df, genre)
        
        # Salva dataset limpo
        output_dir = ml_ready_dir.parent / 'cleaned'
        output_dir.mkdir(exist_ok=True)
        
        output_file = output_dir / f'{genre}_cleaned.csv'
        df_clean.to_csv(output_file, index=False, encoding='utf-8')
        
        print(f"\nDataset limpo salvo: {output_file}")
    
    print(f"\n\n{'='*70}")
    print("VALIDACAO CONCLUIDA!")
    print(f"{'='*70}")
    print("\nProximos passos:")
    print("1. Revisar amostras manualmente")
    print("2. Treinar modelo com datasets limpos:")
    print("   python ml/train_with_cleaned_data.py")

if __name__ == "__main__":
    main()
