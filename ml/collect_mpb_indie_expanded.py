"""
Coleta Expandida: MPB Indie/Alternativa
Meta: +100 músicas para atingir 150-160 total
"""
import pandas as pd
from pathlib import Path

def get_expanded_indie_hits():
    """Hits expandidos de MPB Indie"""
    hits = []
    
    # Mais Silva
    silva_hits = [
        {'track_name': 'Vista Pro Mar', 'artist': 'Silva'},
        {'track_name': 'Claridão', 'artist': 'Silva'},
        {'track_name': 'Não Precisa Mudar', 'artist': 'Silva'},
        {'track_name': 'Fica Tudo Bem', 'artist': 'Silva'},
    ]
    
    # Mais Criolo
    criolo_hits = [
        {'track_name': 'Bogotá', 'artist': 'Criolo'},
        {'track_name': 'Convoque Seu Buda', 'artist': 'Criolo'},
    ]
    
    # Mallu Magalhães
    mallu_hits = [
        {'track_name': 'Tchubaruba', 'artist': 'Mallu Magalhães'},
        {'track_name': 'Velha e Louca', 'artist': 'Mallu Magalhães'},
        {'track_name': 'Você Não Presta', 'artist': 'Mallu Magalhães'},
    ]
    
    # Clarice Falcão
    clarice_hits = [
        {'track_name': 'Macaé', 'artist': 'Clarice Falcão'},
        {'track_name': 'Eu Esqueci Você', 'artist': 'Clarice Falcão'},
        {'track_name': 'Fred Astaire', 'artist': 'Clarice Falcão'},
    ]
    
    # Los Hermanos
    loshermanos_hits = [
        {'track_name': 'Anna Júlia', 'artist': 'Los Hermanos'},
        {'track_name': 'Além do Que Se Vê', 'artist': 'Los Hermanos'},
        {'track_name': 'Primavera', 'artist': 'Los Hermanos'},
    ]
    
    # Terno Rei
    terno_hits = [
        {'track_name': 'Violeta', 'artist': 'O Terno'},
        {'track_name': 'Aí Cê Já Era', 'artist': 'O Terno'},
        {'track_name': 'Profundo', 'artist': 'O Terno'},
    ]
    
    # Maglore
    maglore_hits = [
        {'track_name': 'Enquanto Você Dorme', 'artist': 'Maglore'},
        {'track_name': 'Tudo Pode Mudar', 'artist': 'Maglore'},
    ]
    
    # Mahmundi
    mahmundi_hits = [
        {'track_name': 'Pra Você Dar o Nome', 'artist': 'Mahmundi'},
        {'track_name': 'Lágrimas no Mar', 'artist': 'Mahmundi'},
    ]
    
    # Castello Branco
    castello_hits = [
        {'track_name': 'Eu Quero É Botar Meu Bloco na Rua', 'artist': 'Castello Branco'},
    ]
    
    # Dingo Bells
    dingo_hits = [
        {'track_name': 'Eu Não Sei', 'artist': 'Dingo Bells'},
    ]
    
    # Boogarins
    boogarins_hits = [
        {'track_name': 'Lucifernandis', 'artist': 'Boogarins'},
    ]
    
    # Apanhador Só
    apanhador_hits = [
        {'track_name': 'Antes que Seja Tarde', 'artist': 'Apanhador Só'},
    ]
    
    # Mais Liniker
    liniker_hits = [
        {'track_name': 'Intimidade', 'artist': 'Liniker'},
        {'track_name': 'Baby 95', 'artist': 'Liniker'},
    ]
    
    # Mais Rubel
    rubel_hits = [
        {'track_name': 'Partilhar', 'artist': 'Rubel'},
        {'track_name': 'Grão de Areia', 'artist': 'Rubel'},
    ]
    
    # Mais Céu
    ceu_hits = [
        {'track_name': 'Roda', 'artist': 'Céu'},
        {'track_name': '10 Contados', 'artist': 'Céu'},
    ]
    
    # Mais Tulipa Ruiz
    tulipa_hits = [
        {'track_name': 'Dia a Dia, Lado a Lado', 'artist': 'Tulipa Ruiz'},
    ]
    
    # Mais Tiê
    tie_hits = [
        {'track_name': 'Dois', 'artist': 'Tiê'},
    ]
    
    # Mais Marcelo Jeneci
    jeneci_hits = [
        {'track_name': 'De Graça', 'artist': 'Marcelo Jeneci'},
    ]
    
    all_hits = (silva_hits + criolo_hits + mallu_hits + clarice_hits +
                loshermanos_hits + terno_hits + maglore_hits + mahmundi_hits +
                castello_hits + dingo_hits + boogarins_hits + apanhador_hits +
                liniker_hits + rubel_hits + ceu_hits + tulipa_hits + tie_hits +
                jeneci_hits)
    
    for track in all_hits:
        track['genre'] = 'mpb_indie'
        track['is_hit'] = 1
        track['source'] = 'manual_indie_expanded'
        hits.append(track)
    
    return pd.DataFrame(hits)

def get_expanded_indie_nonhits():
    """Non-hits expandidos de MPB Indie"""
    nonhits = []
    
    # Silva (mais álbum tracks)
    silva_nonhits = [
        {'track_name': 'Tudo Que Eu Não Quero', 'artist': 'Silva'},
        {'track_name': 'Júpiter', 'artist': 'Silva'},
        {'track_name': 'Pra Ser Sincero', 'artist': 'Silva'},
        {'track_name': 'Fica Tudo Bem', 'artist': 'Silva'},
        {'track_name': 'Eu Vou', 'artist': 'Silva'},
    ]
    
    # Criolo (álbum tracks)
    criolo_nonhits = [
        {'track_name': 'Linha de Frente', 'artist': 'Criolo'},
        {'track_name': 'Mariô', 'artist': 'Criolo'},
        {'track_name': 'Espiral de Ilusão', 'artist': 'Criolo'},
        {'track_name': 'Vasilhame', 'artist': 'Criolo'},
    ]
    
    # Mallu Magalhães (álbum tracks)
    mallu_nonhits = [
        {'track_name': 'Sambinha da Bossa', 'artist': 'Mallu Magalhães'},
        {'track_name': 'Janta', 'artist': 'Mallu Magalhães'},
        {'track_name': 'Você Não Presta', 'artist': 'Mallu Magalhães'},
        {'track_name': 'Olha Só', 'artist': 'Mallu Magalhães'},
    ]
    
    # Clarice Falcão (álbum tracks)
    clarice_nonhits = [
        {'track_name': 'Monomania', 'artist': 'Clarice Falcão'},
        {'track_name': 'Talvez', 'artist': 'Clarice Falcão'},
        {'track_name': 'Eu Me Lembro', 'artist': 'Clarice Falcão'},
    ]
    
    # Los Hermanos (álbum tracks)
    loshermanos_nonhits = [
        {'track_name': 'Sentimental', 'artist': 'Los Hermanos'},
        {'track_name': 'O Vencedor', 'artist': 'Los Hermanos'},
        {'track_name': 'Cara Estranho', 'artist': 'Los Hermanos'},
        {'track_name': 'Último Romance', 'artist': 'Los Hermanos'},
    ]
    
    # O Terno (álbum tracks)
    terno_nonhits = [
        {'track_name': '66', 'artist': 'O Terno'},
        {'track_name': 'Deixa Fugir', 'artist': 'O Terno'},
        {'track_name': 'Eu Tomei Coca, Eu Tomei Fanta', 'artist': 'O Terno'},
        {'track_name': 'Olhos Vermelhos', 'artist': 'O Terno'},
    ]
    
    # Maglore (álbum tracks)
    maglore_nonhits = [
        {'track_name': 'Tudo Pode Mudar', 'artist': 'Maglore'},
        {'track_name': 'Ô Sol', 'artist': 'Maglore'},
        {'track_name': 'Paquetá', 'artist': 'Maglore'},
    ]
    
    # Mahmundi (álbum tracks)
    mahmundi_nonhits = [
        {'track_name': 'Nós', 'artist': 'Mahmundi'},
        {'track_name': 'Nada em Vão', 'artist': 'Mahmundi'},
    ]
    
    # Liniker (álbum tracks)
    liniker_nonhits = [
        {'track_name': 'Tua', 'artist': 'Liniker'},
        {'track_name': 'Psiu', 'artist': 'Liniker'},
        {'track_name': 'Presente', 'artist': 'Liniker'},
    ]
    
    # Rubel (álbum tracks)
    rubel_nonhits = [
        {'track_name': 'Asas', 'artist': 'Rubel'},
        {'track_name': 'Quando Bate Aquela Saudade', 'artist': 'Rubel'},
        {'track_name': 'Quadros', 'artist': 'Rubel'},
    ]
    
    # Céu (álbum tracks)
    ceu_nonhits = [
        {'track_name': 'Varanda Suspensa', 'artist': 'Céu'},
        {'track_name': 'Perfume do Invisível', 'artist': 'Céu'},
    ]
    
    # Tulipa Ruiz (álbum tracks)
    tulipa_nonhits = [
        {'track_name': 'Tudo Tanto', 'artist': 'Tulipa Ruiz'},
        {'track_name': 'Só Mais Uma Canção', 'artist': 'Tulipa Ruiz'},
    ]
    
    # Tiê (álbum tracks)
    tie_nonhits = [
        {'track_name': 'Amuleto', 'artist': 'Tiê'},
        {'track_name': 'Pra Curar Essa Dor', 'artist': 'Tiê'},
    ]
    
    # Marcelo Jeneci (álbum tracks)
    jeneci_nonhits = [
        {'track_name': 'Dar-te-ei', 'artist': 'Marcelo Jeneci'},
        {'track_name': 'Dia Branco', 'artist': 'Marcelo Jeneci'},
    ]
    
    # A Banda Mais Bonita (álbum tracks)
    abandmaisb_nonhits = [
        {'track_name': 'Suas Mãos', 'artist': 'A Banda Mais Bonita da Cidade'},
        {'track_name': 'Nunca', 'artist': 'A Banda Mais Bonita da Cidade'},
        {'track_name': 'Canção Pra Não Voltar', 'artist': 'A Banda Mais Bonita da Cidade'},
    ]
    
    # Arnaldo Antunes (álbum tracks)
    arnaldo_nonhits = [
        {'track_name': 'Longe', 'artist': 'Arnaldo Antunes'},
        {'track_name': 'Cultura', 'artist': 'Arnaldo Antunes'},
        {'track_name': 'Saiba', 'artist': 'Arnaldo Antunes'},
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
    
    all_nonhits = (silva_nonhits + criolo_nonhits + mallu_nonhits + clarice_nonhits +
                   loshermanos_nonhits + terno_nonhits + maglore_nonhits + mahmundi_nonhits +
                   liniker_nonhits + rubel_nonhits + ceu_nonhits + tulipa_nonhits +
                   tie_nonhits + jeneci_nonhits + abandmaisb_nonhits + arnaldo_nonhits +
                   zeca_nonhits + lenine_nonhits)
    
    for track in all_nonhits:
        track['genre'] = 'mpb_indie'
        track['is_hit'] = 0
        track['source'] = 'manual_indie_expanded'
        nonhits.append(track)
    
    return pd.DataFrame(nonhits)

def create_mpb_indie_expanded():
    """Cria dataset expandido de MPB Indie"""
    print("\n" + "="*70)
    print("COLETA EXPANDIDA: MPB INDIE/ALTERNATIVA")
    print("="*70 + "\n")
    
    datasets_dir = Path(__file__).parent / 'datasets'
    
    # Carrega base atual
    base_path = datasets_dir / 'mpb_indie_final.csv'
    df_base = pd.read_csv(base_path)
    print(f"Base atual: {len(df_base)} musicas")
    
    # Adiciona hits expandidos
    df_hits = get_expanded_indie_hits()
    print(f"Hits expandidos: {len(df_hits)}")
    
    # Adiciona non-hits expandidos
    df_nonhits = get_expanded_indie_nonhits()
    print(f"Non-hits expandidos: {len(df_nonhits)}")
    
    # Combina
    df_final = pd.concat([df_base, df_hits, df_nonhits], ignore_index=True)
    df_final = df_final.drop_duplicates(subset=['track_name'], keep='first')
    
    # Salva
    output_path = datasets_dir / 'mpb_indie_expanded.csv'
    df_final.to_csv(output_path, index=False)
    
    print(f"\nDataset expandido:")
    print(f"  Total: {len(df_final)} musicas")
    print(f"  Hits: {df_final['is_hit'].sum()} ({df_final['is_hit'].mean():.1%})")
    print(f"  Non-hits: {len(df_final) - df_final['is_hit'].sum()} ({1-df_final['is_hit'].mean():.1%})")
    print(f"  Salvo: {output_path.name}")
    
    print("\n" + "="*70)
    print("MPB INDIE EXPANDIDO PRONTO!")
    print("="*70)
    
    return df_final

if __name__ == "__main__":
    create_mpb_indie_expanded()
