"""
Combinação Final e Retreinamento
Combina hits verificados com datasets existentes e retreina modelos
"""
import pandas as pd
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

def combine_with_existing_datasets():
    """Combina hits verificados com datasets existentes"""
    print("\n" + "="*70)
    print("COMBINANDO HITS VERIFICADOS COM DATASETS EXISTENTES")
    print("="*70 + "\n")
    
    datasets_dir = Path(__file__).parent / 'datasets'
    
    # Carrega hits verificados
    verified_path = datasets_dir / 'verified_hits_complete.csv'
    df_verified = pd.read_csv(verified_path)
    
    print(f"Hits verificados: {len(df_verified)}")
    print(f"Distribuicao: {df_verified['genre'].value_counts().to_dict()}")
    
    # Para cada subcategoria
    subcategories = {
        'mpb_rock': 'mpb_rock_ml.csv',
        'nova_mpb': 'nova_mpb_ml.csv',
        'rnb_trap': 'rnb_trap_ml.csv',
        'rnb_pop': 'rnb_pop_ml.csv'
    }
    
    final_datasets = {}
    
    for genre, filename in subcategories.items():
        print(f"\n{'='*70}")
        print(f"PROCESSANDO: {genre.upper().replace('_', ' ')}")
        print(f"{'='*70}")
        
        # Carrega dataset existente
        existing_path = datasets_dir / filename
        if existing_path.exists():
            df_existing = pd.read_csv(existing_path)
            print(f"Dataset existente: {len(df_existing)} musicas")
        else:
            df_existing = pd.DataFrame()
            print(f"Dataset existente: NAO ENCONTRADO")
        
        # Filtra hits verificados deste gênero
        df_genre_hits = df_verified[df_verified['genre'] == genre].copy()
        print(f"Hits verificados: {len(df_genre_hits)} musicas")
        
        # Combina
        if len(df_existing) > 0:
            df_combined = pd.concat([df_existing, df_genre_hits], ignore_index=True)
        else:
            df_combined = df_genre_hits.copy()
        
        # Remove duplicatas
        dup_cols = ['track_name']
        if 'artist' in df_combined.columns:
            dup_cols.append('artist')
        df_combined = df_combined.drop_duplicates(subset=dup_cols, keep='first')
        
        # Salva dataset final
        final_path = datasets_dir / f"{genre}_final.csv"
        df_combined.to_csv(final_path, index=False)
        
        print(f"Dataset final: {len(df_combined)} musicas")
        print(f"Hit ratio: {df_combined['is_hit'].mean():.1%}")
        print(f"Salvo: {final_path.name}")
        
        final_datasets[genre] = {
            'path': str(final_path),
            'size': len(df_combined),
            'hit_ratio': df_combined['is_hit'].mean()
        }
    
    # Relatório
    print("\n" + "="*70)
    print("RESUMO DOS DATASETS FINAIS")
    print("="*70 + "\n")
    
    for genre, info in final_datasets.items():
        print(f"{genre.upper().replace('_', ' ')}:")
        print(f"  Total: {info['size']} musicas")
        print(f"  Hit ratio: {info['hit_ratio']:.1%}")
        print(f"  Arquivo: {Path(info['path']).name}")
        print()
    
    print("="*70)
    print("DATASETS FINAIS PRONTOS PARA RETREINAMENTO!")
    print("="*70)
    
    return final_datasets

if __name__ == "__main__":
    combine_with_existing_datasets()
