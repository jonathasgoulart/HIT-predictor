"""
Coleta de Non-Hits para MPB Rock
Músicas de rock brasileiro que não foram grandes hits comerciais
"""
import pandas as pd
from pathlib import Path

def get_mpb_rock_nonhits():
    """
    Retorna lista de músicas de MPB Rock que não foram hits comerciais
    Critério: Músicas boas, mas que não alcançaram charts ou grande sucesso comercial
    """
    
    nonhits = []
    
    # ========================================
    # MPB ROCK NON-HITS (~50 músicas)
    # ========================================
    
    # Paralamas do Sucesso (álbum tracks, não singles)
    paralamas_nonhits = [
        {'track_name': 'Caleidoscópio', 'artist': 'Paralamas do Sucesso'},
        {'track_name': 'Quase um Segundo', 'artist': 'Paralamas do Sucesso'},
        {'track_name': 'Patrulha Noturna', 'artist': 'Paralamas do Sucesso'},
        {'track_name': 'Vamo Batê Lata', 'artist': 'Paralamas do Sucesso'},
    ]
    
    # Legião Urbana (álbum tracks)
    legiao_nonhits = [
        {'track_name': 'Angra dos Reis', 'artist': 'Legião Urbana'},
        {'track_name': 'Ainda É Cedo', 'artist': 'Legião Urbana'},
        {'track_name': 'Baader-Meinhof Blues', 'artist': 'Legião Urbana'},
        {'track_name': 'Soldados', 'artist': 'Legião Urbana'},
        {'track_name': 'Química', 'artist': 'Legião Urbana'},
    ]
    
    # Titãs (álbum tracks)
    titas_nonhits = [
        {'track_name': 'Insensível', 'artist': 'Titãs'},
        {'track_name': 'Desordem', 'artist': 'Titãs'},
        {'track_name': 'Televisão', 'artist': 'Titãs'},
        {'track_name': 'Família', 'artist': 'Titãs'},
        {'track_name': 'Lugar Nenhum', 'artist': 'Titãs'},
    ]
    
    # Cazuza/Barão Vermelho (álbum tracks)
    cazuza_nonhits = [
        {'track_name': 'Down em Mim', 'artist': 'Cazuza'},
        {'track_name': 'Medieval II', 'artist': 'Cazuza'},
        {'track_name': 'Blues da Piedade', 'artist': 'Cazuza'},
        {'track_name': 'Maior Abandonado', 'artist': 'Barão Vermelho'},
    ]
    
    # Engenheiros do Hawaii (álbum tracks)
    engenheiros_nonhits = [
        {'track_name': 'Toda Forma de Poder', 'artist': 'Engenheiros do Hawaii'},
        {'track_name': 'Nau à Deriva', 'artist': 'Engenheiros do Hawaii'},
        {'track_name': 'Surfando Karmas e DNA', 'artist': 'Engenheiros do Hawaii'},
        {'track_name': 'O Papa É Pop', 'artist': 'Engenheiros do Hawaii'},
    ]
    
    # Capital Inicial (álbum tracks)
    capital_nonhits = [
        {'track_name': 'Psicopata', 'artist': 'Capital Inicial'},
        {'track_name': 'Kamikaze', 'artist': 'Capital Inicial'},
        {'track_name': 'Leve Desespero', 'artist': 'Capital Inicial'},
    ]
    
    # Ira! (álbum tracks)
    ira_nonhits = [
        {'track_name': 'Tolices', 'artist': 'Ira!'},
        {'track_name': 'Receita Para Se Fazer Um Herói', 'artist': 'Ira!'},
        {'track_name': 'Gritos na Multidão', 'artist': 'Ira!'},
    ]
    
    # Ultraje a Rigor (álbum tracks)
    ultraje_nonhits = [
        {'track_name': 'Rebelde Sem Causa', 'artist': 'Ultraje a Rigor'},
        {'track_name': 'Ciúme', 'artist': 'Ultraje a Rigor'},
        {'track_name': 'Marylou', 'artist': 'Ultraje a Rigor'},
    ]
    
    # RPM (álbum tracks)
    rpm_nonhits = [
        {'track_name': 'Revoluções Por Minuto', 'artist': 'RPM'},
        {'track_name': 'Vida Real', 'artist': 'RPM'},
        {'track_name': 'Alvorada Voraz', 'artist': 'RPM'},
    ]
    
    # Skank (álbum tracks)
    skank_nonhits = [
        {'track_name': 'É Proibido Fumar', 'artist': 'Skank'},
        {'track_name': 'Hollywood', 'artist': 'Skank'},
        {'track_name': 'Pacato Cidadão', 'artist': 'Skank'},
    ]
    
    # Charlie Brown Jr (álbum tracks)
    charlie_nonhits = [
        {'track_name': 'Papo Reto', 'artist': 'Charlie Brown Jr'},
        {'track_name': 'Senhor do Tempo', 'artist': 'Charlie Brown Jr'},
        {'track_name': 'Confisco', 'artist': 'Charlie Brown Jr'},
    ]
    
    # Los Hermanos (álbum tracks)
    loshermanos_nonhits = [
        {'track_name': 'Sentimental', 'artist': 'Los Hermanos'},
        {'track_name': 'O Vencedor', 'artist': 'Los Hermanos'},
        {'track_name': 'Cara Estranho', 'artist': 'Los Hermanos'},
    ]
    
    # O Rappa (álbum tracks)
    orappa_nonhits = [
        {'track_name': 'Reza Vela', 'artist': 'O Rappa'},
        {'track_name': 'Instinto Coletivo', 'artist': 'O Rappa'},
        {'track_name': 'Lado B Lado A', 'artist': 'O Rappa'},
    ]
    
    # Detonautas (álbum tracks)
    detonautas_nonhits = [
        {'track_name': 'O Dia Que Não Terminou', 'artist': 'Detonautas'},
        {'track_name': 'Outro Lugar', 'artist': 'Detonautas'},
    ]
    
    # NX Zero (álbum tracks)
    nxzero_nonhits = [
        {'track_name': 'Cartas Pra Você', 'artist': 'NX Zero'},
        {'track_name': 'Daqui Pra Frente', 'artist': 'NX Zero'},
    ]
    
    # Fresno (álbum tracks)
    fresno_nonhits = [
        {'track_name': 'Quebre as Correntes', 'artist': 'Fresno'},
        {'track_name': 'Alguém Que Te Faz Sorrir', 'artist': 'Fresno'},
    ]
    
    # Combina todas as listas
    all_nonhits = (paralamas_nonhits + legiao_nonhits + titas_nonhits + 
                   cazuza_nonhits + engenheiros_nonhits + capital_nonhits +
                   ira_nonhits + ultraje_nonhits + rpm_nonhits + skank_nonhits +
                   charlie_nonhits + loshermanos_nonhits + orappa_nonhits +
                   detonautas_nonhits + nxzero_nonhits + fresno_nonhits)
    
    # Adiciona metadados
    for track in all_nonhits:
        track['genre'] = 'mpb_rock'
        track['is_hit'] = 0  # NON-HIT
        track['source'] = 'manual_nonhit_collection'
        nonhits.append(track)
    
    df = pd.DataFrame(nonhits)
    return df

def combine_with_mpb_rock():
    """Combina non-hits com dataset MPB Rock existente"""
    print("\n" + "="*70)
    print("ADICIONANDO NON-HITS AO MPB ROCK")
    print("="*70 + "\n")
    
    datasets_dir = Path(__file__).parent / 'datasets'
    
    # Carrega non-hits
    df_nonhits = get_mpb_rock_nonhits()
    print(f"Non-hits coletados: {len(df_nonhits)}")
    
    # Carrega dataset MPB Rock atual
    mpb_rock_path = datasets_dir / 'mpb_rock_final.csv'
    if mpb_rock_path.exists():
        df_mpb_rock = pd.read_csv(mpb_rock_path)
        print(f"Dataset MPB Rock atual: {len(df_mpb_rock)} musicas ({df_mpb_rock['is_hit'].mean():.1%} hits)")
    else:
        print("Dataset MPB Rock nao encontrado")
        return None
    
    # Combina
    df_combined = pd.concat([df_mpb_rock, df_nonhits], ignore_index=True)
    
    # Remove duplicatas
    dup_cols = ['track_name']
    if 'artist' in df_combined.columns:
        dup_cols.append('artist')
    df_combined = df_combined.drop_duplicates(subset=dup_cols, keep='first')
    
    # Salva dataset balanceado
    balanced_path = datasets_dir / 'mpb_rock_balanced_v2.csv'
    df_combined.to_csv(balanced_path, index=False)
    
    print(f"\nDataset balanceado:")
    print(f"  Total: {len(df_combined)} musicas")
    print(f"  Hits: {df_combined['is_hit'].sum()}")
    print(f"  Non-hits: {len(df_combined) - df_combined['is_hit'].sum()}")
    print(f"  Hit ratio: {df_combined['is_hit'].mean():.1%}")
    print(f"  Salvo: {balanced_path.name}")
    
    print("\n" + "="*70)
    print("MPB ROCK BALANCEADO!")
    print("="*70)
    
    return balanced_path

if __name__ == "__main__":
    combine_with_mpb_rock()
