"""
Coleta Massiva: MPB Indie/Alternativa
Foco em artistas indie, alternativos e contemporâneos brasileiros
"""
import pandas as pd
from pathlib import Path

def get_mpb_indie_hits():
    """Hits de MPB Indie/Alternativa"""
    hits = []
    
    # Silva
    silva_hits = [
        {'track_name': 'Pra Você Dar o Nome', 'artist': 'Silva'},
        {'track_name': 'Feliz e Ponto', 'artist': 'Silva'},
        {'track_name': 'Não Precisa Mudar', 'artist': 'Silva'},
    ]
    
    # Criolo
    criolo_hits = [
        {'track_name': 'Não Existe Amor em SP', 'artist': 'Criolo'},
        {'track_name': 'Subirusdoistiozin', 'artist': 'Criolo'},
    ]
    
    # A Banda Mais Bonita da Cidade
    abandmaisb_hits = [
        {'track_name': 'Oração', 'artist': 'A Banda Mais Bonita da Cidade'},
        {'track_name': 'Terminei Indo', 'artist': 'A Banda Mais Bonita da Cidade'},
    ]
    
    # Céu
    ceu_hits = [
        {'track_name': 'Lenda', 'artist': 'Céu'},
        {'track_name': 'Concrete Jungle', 'artist': 'Céu'},
    ]
    
    # Tulipa Ruiz
    tulipa_hits = [
        {'track_name': 'Efêmera', 'artist': 'Tulipa Ruiz'},
        {'track_name': 'Só Sei Dançar Com Você', 'artist': 'Tulipa Ruiz'},
    ]
    
    # Tiê
    tie_hits = [
        {'track_name': 'A Noite', 'artist': 'Tiê'},
        {'track_name': 'Mexeu Comigo', 'artist': 'Tiê'},
    ]
    
    # Liniker
    liniker_hits = [
        {'track_name': 'Zero', 'artist': 'Liniker'},
        {'track_name': 'Lalange', 'artist': 'Liniker'},
    ]
    
    # Rubel
    rubel_hits = [
        {'track_name': 'Quando Bate Aquela Saudade', 'artist': 'Rubel'},
        {'track_name': 'Asas', 'artist': 'Rubel'},
    ]
    
    # Marcelo Jeneci
    jeneci_hits = [
        {'track_name': 'Felicidade', 'artist': 'Marcelo Jeneci'},
        {'track_name': 'Pra Sonhar', 'artist': 'Marcelo Jeneci'},
    ]
    
    # Arnaldo Antunes
    arnaldo_hits = [
        {'track_name': 'Volte Para o Seu Lar', 'artist': 'Arnaldo Antunes'},
        {'track_name': 'O Pulso', 'artist': 'Arnaldo Antunes'},
    ]
    
    # Zeca Baleiro
    zeca_hits = [
        {'track_name': 'Samba do Approach', 'artist': 'Zeca Baleiro'},
        {'track_name': 'Telegrama', 'artist': 'Zeca Baleiro'},
    ]
    
    # Lenine
    lenine_hits = [
        {'track_name': 'Paciência', 'artist': 'Lenine'},
        {'track_name': 'A Ponte', 'artist': 'Lenine'},
    ]
    
    # Emicida (quando não é trap)
    emicida_hits = [
        {'track_name': 'Passarinhos', 'artist': 'Emicida'},
        {'track_name': 'Boa Esperança', 'artist': 'Emicida'},
    ]
    
    all_hits = (silva_hits + criolo_hits + abandmaisb_hits + ceu_hits +
                tulipa_hits + tie_hits + liniker_hits + rubel_hits +
                jeneci_hits + arnaldo_hits + zeca_hits + lenine_hits +
                emicida_hits)
    
    for track in all_hits:
        track['genre'] = 'mpb_indie'
        track['is_hit'] = 1
        track['source'] = 'manual_indie_collection'
        hits.append(track)
    
    return pd.DataFrame(hits)

def get_mpb_indie_nonhits():
    """Non-hits de MPB Indie/Alternativa"""
    nonhits = []
    
    # Silva (álbum tracks)
    silva_nonhits = [
        {'track_name': 'Júpiter', 'artist': 'Silva'},
        {'track_name': 'Tudo Que Eu Não Quero', 'artist': 'Silva'},
        {'track_name': 'Pra Ser Sincero', 'artist': 'Silva'},
        {'track_name': 'Fica Tudo Bem', 'artist': 'Silva'},
    ]
    
    # Criolo (álbum tracks)
    criolo_nonhits = [
        {'track_name': 'Linha de Frente', 'artist': 'Criolo'},
        {'track_name': 'Mariô', 'artist': 'Criolo'},
        {'track_name': 'Bogotá', 'artist': 'Criolo'},
    ]
    
    # A Banda Mais Bonita (álbum tracks)
    abandmaisb_nonhits = [
        {'track_name': 'Suas Mãos', 'artist': 'A Banda Mais Bonita da Cidade'},
        {'track_name': 'Nunca', 'artist': 'A Banda Mais Bonita da Cidade'},
    ]
    
    # Céu (álbum tracks)
    ceu_nonhits = [
        {'track_name': 'Varanda Suspensa', 'artist': 'Céu'},
        {'track_name': 'Roda', 'artist': 'Céu'},
    ]
    
    # Tulipa Ruiz (álbum tracks)
    tulipa_nonhits = [
        {'track_name': 'Dia a Dia, Lado a Lado', 'artist': 'Tulipa Ruiz'},
        {'track_name': 'Tudo Tanto', 'artist': 'Tulipa Ruiz'},
    ]
    
    # Tiê (álbum tracks)
    tie_nonhits = [
        {'track_name': 'Dois', 'artist': 'Tiê'},
        {'track_name': 'Amuleto', 'artist': 'Tiê'},
    ]
    
    # Liniker (álbum tracks)
    liniker_nonhits = [
        {'track_name': 'Tua', 'artist': 'Liniker'},
        {'track_name': 'Psiu', 'artist': 'Liniker'},
    ]
    
    # Rubel (álbum tracks)
    rubel_nonhits = [
        {'track_name': 'Partilhar', 'artist': 'Rubel'},
        {'track_name': 'Grão de Areia', 'artist': 'Rubel'},
    ]
    
    # Marcelo Jeneci (álbum tracks)
    jeneci_nonhits = [
        {'track_name': 'De Graça', 'artist': 'Marcelo Jeneci'},
        {'track_name': 'Dar-te-ei', 'artist': 'Marcelo Jeneci'},
    ]
    
    # Arnaldo Antunes (álbum tracks)
    arnaldo_nonhits = [
        {'track_name': 'Longe', 'artist': 'Arnaldo Antunes'},
        {'track_name': 'Cultura', 'artist': 'Arnaldo Antunes'},
    ]
    
    # Zeca Baleiro (álbum tracks)
    zeca_nonhits = [
        {'track_name': 'Heavy Metal do Senhor', 'artist': 'Zeca Baleiro'},
        {'track_name': 'Babylon', 'artist': 'Zeca Baleiro'},
    ]
    
    # Lenine (álbum tracks)
    lenine_nonhits = [
        {'track_name': 'Jack Soul Brasileiro', 'artist': 'Lenine'},
        {'track_name': 'O Último Pôr do Sol', 'artist': 'Lenine'},
    ]
    
    all_nonhits = (silva_nonhits + criolo_nonhits + abandmaisb_nonhits +
                   ceu_nonhits + tulipa_nonhits + tie_nonhits +
                   liniker_nonhits + rubel_nonhits + jeneci_nonhits +
                   arnaldo_nonhits + zeca_nonhits + lenine_nonhits)
    
    for track in all_nonhits:
        track['genre'] = 'mpb_indie'
        track['is_hit'] = 0
        track['source'] = 'manual_indie_collection'
        nonhits.append(track)
    
    return pd.DataFrame(nonhits)

def create_mpb_indie_final():
    """Cria dataset final de MPB Indie"""
    print("\n" + "="*70)
    print("CRIANDO DATASET FINAL: MPB INDIE/ALTERNATIVA")
    print("="*70 + "\n")
    
    datasets_dir = Path(__file__).parent / 'datasets'
    
    # Carrega base filtrada
    base_path = datasets_dir / 'mpb_indie_base.csv'
    df_base = pd.read_csv(base_path)
    print(f"Base filtrada: {len(df_base)} musicas")
    
    # Adiciona hits
    df_hits = get_mpb_indie_hits()
    print(f"Hits coletados: {len(df_hits)}")
    
    # Adiciona non-hits
    df_nonhits = get_mpb_indie_nonhits()
    print(f"Non-hits coletados: {len(df_nonhits)}")
    
    # Combina
    df_final = pd.concat([df_base, df_hits, df_nonhits], ignore_index=True)
    df_final = df_final.drop_duplicates(subset=['track_name'], keep='first')
    
    # Salva
    output_path = datasets_dir / 'mpb_indie_final.csv'
    df_final.to_csv(output_path, index=False)
    
    print(f"\nDataset final:")
    print(f"  Total: {len(df_final)} musicas")
    print(f"  Hits: {df_final['is_hit'].sum()} ({df_final['is_hit'].mean():.1%})")
    print(f"  Non-hits: {len(df_final) - df_final['is_hit'].sum()} ({1-df_final['is_hit'].mean():.1%})")
    print(f"  Salvo: {output_path.name}")
    
    print("\n" + "="*70)
    print("MPB INDIE FINAL PRONTO!")
    print("="*70)
    
    return df_final

if __name__ == "__main__":
    create_mpb_indie_final()
