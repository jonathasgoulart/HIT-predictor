"""
Refatoração: Nova MPB → MPB Indie/Alternativa
Remove músicas clássicas/bossa, mantém apenas indie/alternativa
"""
import pandas as pd
from pathlib import Path

def filter_indie_only():
    """Filtra apenas artistas indie/alternativos"""
    datasets_dir = Path(__file__).parent / 'datasets'
    
    print("\n" + "="*70)
    print("REFATORACAO: NOVA MPB -> MPB INDIE/ALTERNATIVA")
    print("="*70 + "\n")
    
    # Carrega dataset atual
    nova_mpb_path = datasets_dir / 'nova_mpb_precision.csv'
    df = pd.read_csv(nova_mpb_path)
    
    print(f"Dataset atual: {len(df)} musicas")
    print(f"Hits: {df['is_hit'].sum()} | Non-hits: {len(df) - df['is_hit'].sum()}")
    
    # Artistas INDIE/ALTERNATIVOS (manter)
    indie_artists = [
        'Silva', 'Criolo', 'A Banda Mais Bonita da Cidade',
        'Emicida', 'Tulipa Ruiz', 'Céu', 'Tiê',
        'Arnaldo Antunes', 'Zeca Baleiro', 'Lenine'
    ]
    
    # Artistas CLÁSSICOS/BOSSA (remover)
    classic_artists = [
        'Chico Buarque', 'Caetano Veloso', 'Gilberto Gil',
        'Tom Jobim', 'João Gilberto', 'Elis Regina',
        'Gal Costa', 'Maria Bethânia', 'Milton Nascimento',
        'Djavan', 'Marisa Monte'
    ]
    
    # Filtra apenas indie
    def is_indie(row):
        if 'artist' not in row or pd.isna(row['artist']):
            return False
        
        artist = str(row['artist']).lower()
        
        # Verifica se é indie
        for indie in indie_artists:
            if indie.lower() in artist:
                return True
        
        # Verifica se é clássico (remove)
        for classic in classic_artists:
            if classic.lower() in artist:
                return False
        
        # Se não reconheceu, assume indie (conservador)
        return True
    
    df_indie = df[df.apply(is_indie, axis=1)].copy()
    df_classic = df[~df.apply(is_indie, axis=1)].copy()
    
    print(f"\nAPOS FILTRAGEM:")
    print(f"MPB Indie: {len(df_indie)} musicas")
    print(f"  Hits: {df_indie['is_hit'].sum()} | Non-hits: {len(df_indie) - df_indie['is_hit'].sum()}")
    print(f"  Hit ratio: {df_indie['is_hit'].mean():.1%}")
    
    print(f"\nMPB Classica (removidas): {len(df_classic)} musicas")
    print(f"  Hits: {df_classic['is_hit'].sum()} | Non-hits: {len(df_classic) - df_classic['is_hit'].sum()}")
    
    # Salva MPB Indie
    indie_path = datasets_dir / 'mpb_indie_base.csv'
    df_indie.to_csv(indie_path, index=False)
    print(f"\nSalvo: {indie_path.name}")
    
    # Salva MPB Clássica (para uso futuro)
    classic_path = datasets_dir / 'mpb_classica_removed.csv'
    df_classic.to_csv(classic_path, index=False)
    print(f"Salvo (removidas): {classic_path.name}")
    
    print("\n" + "="*70)
    print("REFATORACAO CONCLUIDA!")
    print("="*70)
    
    return df_indie, df_classic

if __name__ == "__main__":
    filter_indie_only()
