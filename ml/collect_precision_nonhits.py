"""
Coleta de Non-Hits para Nova MPB e R&B Pop
Foco em máxima precisão através de datasets balanceados
"""
import pandas as pd
from pathlib import Path

def get_nova_mpb_nonhits():
    """
    Non-hits de Nova MPB: indie, alternativo, bossa, MPB clássica
    Músicas de qualidade mas sem sucesso comercial massivo
    """
    
    nonhits = []
    
    # Silva (álbum tracks)
    silva_nonhits = [
        {'track_name': 'Tudo Que Eu Não Quero', 'artist': 'Silva'},
        {'track_name': 'Júpiter', 'artist': 'Silva'},
        {'track_name': 'Pra Ser Sincero', 'artist': 'Silva'},
        {'track_name': 'Fica Tudo Bem', 'artist': 'Silva'},
    ]
    
    # Criolo (álbum tracks)
    criolo_nonhits = [
        {'track_name': 'Linha de Frente', 'artist': 'Criolo'},
        {'track_name': 'Mariô', 'artist': 'Criolo'},
        {'track_name': 'Espiral de Ilusão', 'artist': 'Criolo'},
    ]
    
    # A Banda Mais Bonita da Cidade (álbum tracks)
    abandmaisb_nonhits = [
        {'track_name': 'Suas Mãos', 'artist': 'A Banda Mais Bonita da Cidade'},
        {'track_name': 'Nunca', 'artist': 'A Banda Mais Bonita da Cidade'},
        {'track_name': 'Canção Pra Não Voltar', 'artist': 'A Banda Mais Bonita da Cidade'},
    ]
    
    # Chico Buarque (álbum tracks menos conhecidos)
    chico_nonhits = [
        {'track_name': 'Partido Alto', 'artist': 'Chico Buarque'},
        {'track_name': 'Homenagem ao Malandro', 'artist': 'Chico Buarque'},
        {'track_name': 'Meu Caro Amigo', 'artist': 'Chico Buarque'},
    ]
    
    # Caetano Veloso (álbum tracks)
    caetano_nonhits = [
        {'track_name': 'Terra', 'artist': 'Caetano Veloso'},
        {'track_name': 'Cucurrucucu Paloma', 'artist': 'Caetano Veloso'},
        {'track_name': 'Reconvexo', 'artist': 'Caetano Veloso'},
    ]
    
    # Gilberto Gil (álbum tracks)
    gil_nonhits = [
        {'track_name': 'Refazenda', 'artist': 'Gilberto Gil'},
        {'track_name': 'Drão', 'artist': 'Gilberto Gil'},
        {'track_name': 'Palco', 'artist': 'Gilberto Gil'},
    ]
    
    # Djavan (álbum tracks)
    djavan_nonhits = [
        {'track_name': 'Lilás', 'artist': 'Djavan'},
        {'track_name': 'Nem Um Dia', 'artist': 'Djavan'},
        {'track_name': 'Esquinas', 'artist': 'Djavan'},
    ]
    
    # Marisa Monte (álbum tracks)
    marisa_nonhits = [
        {'track_name': 'Diariamente', 'artist': 'Marisa Monte'},
        {'track_name': 'Infinito Particular', 'artist': 'Marisa Monte'},
    ]
    
    # Lenine (álbum tracks)
    lenine_nonhits = [
        {'track_name': 'Jack Soul Brasileiro', 'artist': 'Lenine'},
        {'track_name': 'O Último Pôr do Sol', 'artist': 'Lenine'},
    ]
    
    # Zeca Baleiro (álbum tracks)
    zeca_nonhits = [
        {'track_name': 'Heavy Metal do Senhor', 'artist': 'Zeca Baleiro'},
        {'track_name': 'Babylon', 'artist': 'Zeca Baleiro'},
    ]
    
    # Arnaldo Antunes (álbum tracks)
    arnaldo_nonhits = [
        {'track_name': 'Longe', 'artist': 'Arnaldo Antunes'},
        {'track_name': 'Cultura', 'artist': 'Arnaldo Antunes'},
    ]
    
    all_nonhits = (silva_nonhits + criolo_nonhits + abandmaisb_nonhits +
                   chico_nonhits + caetano_nonhits + gil_nonhits +
                   djavan_nonhits + marisa_nonhits + lenine_nonhits +
                   zeca_nonhits + arnaldo_nonhits)
    
    for track in all_nonhits:
        track['genre'] = 'nova_mpb'
        track['is_hit'] = 0
        track['source'] = 'manual_nonhit_precision'
        nonhits.append(track)
    
    return pd.DataFrame(nonhits)

def get_rnb_pop_nonhits():
    """
    Non-hits de R&B Pop: pop alternativo brasileiro
    Músicas de qualidade mas sem grande sucesso comercial
    """
    
    nonhits = []
    
    # Vitor Kley (álbum tracks)
    vitor_nonhits = [
        {'track_name': 'Farol das Estrelas', 'artist': 'Vitor Kley'},
        {'track_name': 'Eclipse', 'artist': 'Vitor Kley'},
        {'track_name': 'Adrenalizou', 'artist': 'Vitor Kley'},
    ]
    
    # Tiago Iorc (álbum tracks)
    tiago_nonhits = [
        {'track_name': 'Dia Especial', 'artist': 'Tiago Iorc'},
        {'track_name': 'Bilhetes', 'artist': 'Tiago Iorc'},
        {'track_name': 'Tangerina', 'artist': 'Tiago Iorc'},
    ]
    
    # Melim (álbum tracks)
    melim_nonhits = [
        {'track_name': 'Dois Corações', 'artist': 'Melim'},
        {'track_name': 'Sabe Lá', 'artist': 'Melim'},
    ]
    
    # Lagum (álbum tracks)
    lagum_nonhits = [
        {'track_name': 'Reggae Bom Demais', 'artist': 'Lagum'},
        {'track_name': 'Oi', 'artist': 'Lagum'},
    ]
    
    # Anavitória (álbum tracks)
    anavitoria_nonhits = [
        {'track_name': 'Agora Eu Quero Ir', 'artist': 'Anavitória'},
        {'track_name': 'Singular', 'artist': 'Anavitória'},
    ]
    
    # Atitude 67 (álbum tracks)
    atitude_nonhits = [
        {'track_name': 'Vem Pra Minha Vida', 'artist': 'Atitude 67'},
        {'track_name': 'Saideira', 'artist': 'Atitude 67'},
    ]
    
    # Thiaguinho (álbum tracks)
    thiaguinho_nonhits = [
        {'track_name': 'Falta Você', 'artist': 'Thiaguinho'},
        {'track_name': 'Buquê de Flores', 'artist': 'Thiaguinho'},
    ]
    
    # Sorriso Maroto (álbum tracks)
    sorriso_nonhits = [
        {'track_name': 'Sinais', 'artist': 'Sorriso Maroto'},
        {'track_name': 'Vai e Chora', 'artist': 'Sorriso Maroto'},
    ]
    
    # Dilsinho (álbum tracks)
    dilsinho_nonhits = [
        {'track_name': '12 Horas', 'artist': 'Dilsinho'},
        {'track_name': 'Refém', 'artist': 'Dilsinho'},
    ]
    
    all_nonhits = (vitor_nonhits + tiago_nonhits + melim_nonhits +
                   lagum_nonhits + anavitoria_nonhits + atitude_nonhits +
                   thiaguinho_nonhits + sorriso_nonhits + dilsinho_nonhits)
    
    for track in all_nonhits:
        track['genre'] = 'rnb_pop'
        track['is_hit'] = 0
        track['source'] = 'manual_nonhit_precision'
        nonhits.append(track)
    
    return pd.DataFrame(nonhits)

def balance_for_precision():
    """Balanceia datasets para máxima precisão"""
    print("\n" + "="*70)
    print("BALANCEAMENTO PARA MAXIMA PRECISAO")
    print("="*70 + "\n")
    
    datasets_dir = Path(__file__).parent / 'datasets'
    
    # Nova MPB
    print("NOVA MPB:")
    nova_mpb_nonhits = get_nova_mpb_nonhits()
    print(f"  Non-hits coletados: {len(nova_mpb_nonhits)}")
    
    nova_mpb_path = datasets_dir / 'nova_mpb_balanced.csv'
    if nova_mpb_path.exists():
        df_nova_mpb = pd.read_csv(nova_mpb_path)
        print(f"  Dataset atual: {len(df_nova_mpb)} ({df_nova_mpb['is_hit'].mean():.1%} hits)")
        
        df_nova_mpb_final = pd.concat([df_nova_mpb, nova_mpb_nonhits], ignore_index=True)
        df_nova_mpb_final = df_nova_mpb_final.drop_duplicates(subset=['track_name'], keep='first')
        
        output_path = datasets_dir / 'nova_mpb_precision.csv'
        df_nova_mpb_final.to_csv(output_path, index=False)
        
        print(f"  Dataset final: {len(df_nova_mpb_final)} ({df_nova_mpb_final['is_hit'].mean():.1%} hits)")
        print(f"  Hits: {df_nova_mpb_final['is_hit'].sum()} | Non-hits: {len(df_nova_mpb_final) - df_nova_mpb_final['is_hit'].sum()}")
        print(f"  Salvo: {output_path.name}")
    
    # R&B Pop
    print("\nR&B POP:")
    rnb_pop_nonhits = get_rnb_pop_nonhits()
    print(f"  Non-hits coletados: {len(rnb_pop_nonhits)}")
    
    rnb_pop_path = datasets_dir / 'rnb_pop_balanced.csv'
    if rnb_pop_path.exists():
        df_rnb_pop = pd.read_csv(rnb_pop_path)
        print(f"  Dataset atual: {len(df_rnb_pop)} ({df_rnb_pop['is_hit'].mean():.1%} hits)")
        
        df_rnb_pop_final = pd.concat([df_rnb_pop, rnb_pop_nonhits], ignore_index=True)
        df_rnb_pop_final = df_rnb_pop_final.drop_duplicates(subset=['track_name'], keep='first')
        
        output_path = datasets_dir / 'rnb_pop_precision.csv'
        df_rnb_pop_final.to_csv(output_path, index=False)
        
        print(f"  Dataset final: {len(df_rnb_pop_final)} ({df_rnb_pop_final['is_hit'].mean():.1%} hits)")
        print(f"  Hits: {df_rnb_pop_final['is_hit'].sum()} | Non-hits: {len(df_rnb_pop_final) - df_rnb_pop_final['is_hit'].sum()}")
        print(f"  Salvo: {output_path.name}")
    
    print("\n" + "="*70)
    print("DATASETS BALANCEADOS PARA PRECISAO!")
    print("="*70)

if __name__ == "__main__":
    balance_for_precision()
