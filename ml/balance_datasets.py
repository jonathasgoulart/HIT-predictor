"""
Reclassificação de Non-Hits para Subcategorias
Balanceia datasets adicionando non-hits classificados
"""
import pandas as pd
from pathlib import Path

def reclassify_nonhits():
    """Reclassifica non-hits dos datasets originais para subcategorias"""
    print("\n" + "="*70)
    print("RECLASSIFICACAO DE NON-HITS PARA SUBCATEGORIAS")
    print("="*70 + "\n")
    
    datasets_dir = Path(__file__).parent / 'datasets'
    
    # ========================================
    # MPB: Reclassificar para MPB Rock e Nova MPB
    # ========================================
    print("PROCESSANDO MPB...")
    mpb_original = datasets_dir / 'kaggle_mpb_ml.csv'
    
    if mpb_original.exists():
        df_mpb = pd.read_csv(mpb_original)
        df_mpb_nonhits = df_mpb[df_mpb['is_hit'] == 0].copy()
        
        print(f"MPB non-hits encontrados: {len(df_mpb_nonhits)}")
        
        # Classifica non-hits baseado em features
        def classify_mpb_nonhit(row):
            # MPB Rock: alta energia + loudness alto
            if 'energy' in row and 'loudness' in row:
                if row['energy'] > 0.65 and row['loudness'] > -8:
                    return 'mpb_rock'
            # Default: Nova MPB
            return 'nova_mpb'
        
        df_mpb_nonhits['subgenre'] = df_mpb_nonhits.apply(classify_mpb_nonhit, axis=1)
        
        # Separa
        mpb_rock_nonhits = df_mpb_nonhits[df_mpb_nonhits['subgenre'] == 'mpb_rock'].drop('subgenre', axis=1)
        nova_mpb_nonhits = df_mpb_nonhits[df_mpb_nonhits['subgenre'] == 'nova_mpb'].drop('subgenre', axis=1)
        
        print(f"  MPB Rock non-hits: {len(mpb_rock_nonhits)}")
        print(f"  Nova MPB non-hits: {len(nova_mpb_nonhits)}")
    else:
        mpb_rock_nonhits = pd.DataFrame()
        nova_mpb_nonhits = pd.DataFrame()
        print("MPB original nao encontrado")
    
    # ========================================
    # R&B: Reclassificar para R&B Trap e R&B Pop
    # ========================================
    print("\nPROCESSANDO R&B BRASIL...")
    rnb_original = datasets_dir / 'kaggle_rnb_ml.csv'
    
    if rnb_original.exists():
        df_rnb = pd.read_csv(rnb_original)
        df_rnb_nonhits = df_rnb[df_rnb['is_hit'] == 0].copy()
        
        print(f"R&B non-hits encontrados: {len(df_rnb_nonhits)}")
        
        # Classifica non-hits
        def classify_rnb_nonhit(row):
            if 'bpm' in row and 'speechiness' in row and 'valence' in row:
                # R&B Trap: BPM baixo + alta speechiness
                if row['bpm'] < 95 and row['speechiness'] > 0.15:
                    return 'rnb_trap'
                # R&B Pop: BPM médio + baixa speechiness
                elif row['bpm'] >= 95 and row['speechiness'] < 0.15 and row['valence'] > 0.4:
                    return 'rnb_pop'
            # Default: R&B Trap (maioria)
            return 'rnb_trap'
        
        df_rnb_nonhits['subgenre'] = df_rnb_nonhits.apply(classify_rnb_nonhit, axis=1)
        
        # Separa
        rnb_trap_nonhits = df_rnb_nonhits[df_rnb_nonhits['subgenre'] == 'rnb_trap'].drop('subgenre', axis=1)
        rnb_pop_nonhits = df_rnb_nonhits[df_rnb_nonhits['subgenre'] == 'rnb_pop'].drop('subgenre', axis=1)
        
        print(f"  R&B Trap non-hits: {len(rnb_trap_nonhits)}")
        print(f"  R&B Pop non-hits: {len(rnb_pop_nonhits)}")
    else:
        rnb_trap_nonhits = pd.DataFrame()
        rnb_pop_nonhits = pd.DataFrame()
        print("R&B original nao encontrado")
    
    # ========================================
    # Combina com datasets finais
    # ========================================
    print("\n" + "="*70)
    print("COMBINANDO NON-HITS COM DATASETS FINAIS")
    print("="*70 + "\n")
    
    subcategories = {
        'mpb_rock': (mpb_rock_nonhits, 'mpb_rock_final.csv'),
        'nova_mpb': (nova_mpb_nonhits, 'nova_mpb_final.csv'),
        'rnb_trap': (rnb_trap_nonhits, 'rnb_trap_final.csv'),
        'rnb_pop': (rnb_pop_nonhits, 'rnb_pop_final.csv')
    }
    
    balanced_datasets = {}
    
    for genre, (nonhits_df, filename) in subcategories.items():
        print(f"BALANCEANDO: {genre.upper().replace('_', ' ')}")
        
        # Carrega dataset final atual
        final_path = datasets_dir / filename
        if final_path.exists():
            df_final = pd.read_csv(final_path)
            print(f"  Dataset atual: {len(df_final)} musicas ({df_final['is_hit'].mean():.1%} hits)")
        else:
            print(f"  Dataset nao encontrado: {filename}")
            continue
        
        # Adiciona non-hits
        if len(nonhits_df) > 0:
            df_balanced = pd.concat([df_final, nonhits_df], ignore_index=True)
            
            # Remove duplicatas
            dup_cols = ['track_name']
            if 'artist' in df_balanced.columns:
                dup_cols.append('artist')
            df_balanced = df_balanced.drop_duplicates(subset=dup_cols, keep='first')
            
            # Salva dataset balanceado
            balanced_path = datasets_dir / f"{genre}_balanced.csv"
            df_balanced.to_csv(balanced_path, index=False)
            
            print(f"  Non-hits adicionados: {len(nonhits_df)}")
            print(f"  Dataset balanceado: {len(df_balanced)} musicas ({df_balanced['is_hit'].mean():.1%} hits)")
            print(f"  Salvo: {balanced_path.name}")
            
            balanced_datasets[genre] = {
                'path': str(balanced_path),
                'size': len(df_balanced),
                'hit_ratio': df_balanced['is_hit'].mean()
            }
        else:
            print(f"  Sem non-hits para adicionar")
    
    # Relatório
    print("\n" + "="*70)
    print("RESUMO DOS DATASETS BALANCEADOS")
    print("="*70 + "\n")
    
    for genre, info in balanced_datasets.items():
        print(f"{genre.upper().replace('_', ' ')}:")
        print(f"  Total: {info['size']} musicas")
        print(f"  Hit ratio: {info['hit_ratio']:.1%}")
        print(f"  Arquivo: {Path(info['path']).name}")
        print()
    
    print("="*70)
    print("DATASETS BALANCEADOS PRONTOS!")
    print("="*70)
    
    return balanced_datasets

if __name__ == "__main__":
    reclassify_nonhits()
