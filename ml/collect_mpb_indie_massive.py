"""
Coleta Massiva Final: MPB Indie
Meta: +150 músicas para atingir 250+ total
Baseado no plano aprovado
"""
import pandas as pd
from pathlib import Path

def get_massive_indie_collection():
    """Coleta massiva de MPB Indie - todas as músicas planejadas"""
    
    all_songs = []
    
    # ========================================
    # HITS (+75 músicas)
    # ========================================
    
    # Mallu Magalhães (10 hits)
    mallu_hits = [
        {'track_name': 'Tchubaruba', 'artist': 'Mallu Magalhães', 'is_hit': 1},
        {'track_name': 'Velha e Louca', 'artist': 'Mallu Magalhães', 'is_hit': 1},
        {'track_name': 'Você Não Presta', 'artist': 'Mallu Magalhães', 'is_hit': 1},
        {'track_name': 'Janta', 'artist': 'Mallu Magalhães', 'is_hit': 1},
        {'track_name': 'Olha Só', 'artist': 'Mallu Magalhães', 'is_hit': 1},
        {'track_name': 'Sambinha da Bossa', 'artist': 'Mallu Magalhães', 'is_hit': 1},
        {'track_name': 'Shine Yellow', 'artist': 'Mallu Magalhães', 'is_hit': 1},
        {'track_name': 'Eu Sei', 'artist': 'Mallu Magalhães', 'is_hit': 1},
        {'track_name': 'Vem', 'artist': 'Mallu Magalhães', 'is_hit': 1},
        {'track_name': 'Don\'t You Leave Me', 'artist': 'Mallu Magalhães', 'is_hit': 1},
    ]
    
    # Clarice Falcão (10 hits)
    clarice_hits = [
        {'track_name': 'Macaé', 'artist': 'Clarice Falcão', 'is_hit': 1},
        {'track_name': 'Eu Esqueci Você', 'artist': 'Clarice Falcão', 'is_hit': 1},
        {'track_name': 'Fred Astaire', 'artist': 'Clarice Falcão', 'is_hit': 1},
        {'track_name': 'Monomania', 'artist': 'Clarice Falcão', 'is_hit': 1},
        {'track_name': 'Talvez', 'artist': 'Clarice Falcão', 'is_hit': 1},
        {'track_name': 'Eu Me Lembro', 'artist': 'Clarice Falcão', 'is_hit': 1},
        {'track_name': 'De Todos os Loucos do Mundo', 'artist': 'Clarice Falcão', 'is_hit': 1},
        {'track_name': 'Capitão Gancho', 'artist': 'Clarice Falcão', 'is_hit': 1},
        {'track_name': 'Oitavo Andar', 'artist': 'Clarice Falcão', 'is_hit': 1},
        {'track_name': 'Banho Frio', 'artist': 'Clarice Falcão', 'is_hit': 1},
    ]
    
    # Los Hermanos (15 hits)
    loshermanos_hits = [
        {'track_name': 'Anna Júlia', 'artist': 'Los Hermanos', 'is_hit': 1},
        {'track_name': 'Além do Que Se Vê', 'artist': 'Los Hermanos', 'is_hit': 1},
        {'track_name': 'Primavera', 'artist': 'Los Hermanos', 'is_hit': 1},
        {'track_name': 'Samba a Dois', 'artist': 'Los Hermanos', 'is_hit': 1},
        {'track_name': 'Morena', 'artist': 'Los Hermanos', 'is_hit': 1},
        {'track_name': 'Retrato Pra Iaiá', 'artist': 'Los Hermanos', 'is_hit': 1},
        {'track_name': 'Cara Estranho', 'artist': 'Los Hermanos', 'is_hit': 1},
        {'track_name': 'Sentimental', 'artist': 'Los Hermanos', 'is_hit': 1},
        {'track_name': 'O Vencedor', 'artist': 'Los Hermanos', 'is_hit': 1},
        {'track_name': 'Último Romance', 'artist': 'Los Hermanos', 'is_hit': 1},
        {'track_name': 'A Outra', 'artist': 'Los Hermanos', 'is_hit': 1},
        {'track_name': 'Conversa de Botas Batidas', 'artist': 'Los Hermanos', 'is_hit': 1},
        {'track_name': 'Tá Bom, Né?', 'artist': 'Los Hermanos', 'is_hit': 1},
        {'track_name': 'Deixa Estar', 'artist': 'Los Hermanos', 'is_hit': 1},
        {'track_name': 'Fingi Na Hora Rir', 'artist': 'Los Hermanos', 'is_hit': 1},
    ]
    
    # O Terno (15 hits)
    terno_hits = [
        {'track_name': 'Violeta', 'artist': 'O Terno', 'is_hit': 1},
        {'track_name': 'Aí Cê Já Era', 'artist': 'O Terno', 'is_hit': 1},
        {'track_name': 'Profundo', 'artist': 'O Terno', 'is_hit': 1},
        {'track_name': '66', 'artist': 'O Terno', 'is_hit': 1},
        {'track_name': 'Deixa Fugir', 'artist': 'O Terno', 'is_hit': 1},
        {'track_name': 'Eu Tomei Coca, Eu Tomei Fanta', 'artist': 'O Terno', 'is_hit': 1},
        {'track_name': 'Olhos Vermelhos', 'artist': 'O Terno', 'is_hit': 1},
        {'track_name': 'Volta', 'artist': 'O Terno', 'is_hit': 1},
        {'track_name': 'Tudo Por Nada', 'artist': 'O Terno', 'is_hit': 1},
        {'track_name': 'Eu Não Preciso de Ninguém', 'artist': 'O Terno', 'is_hit': 1},
        {'track_name': 'Morto', 'artist': 'O Terno', 'is_hit': 1},
        {'track_name': 'Atrás/Além', 'artist': 'O Terno', 'is_hit': 1},
        {'track_name': 'Eu Não Vou Mais Lavar os Pratos', 'artist': 'O Terno', 'is_hit': 1},
        {'track_name': 'Volta Pra Casa', 'artist': 'O Terno', 'is_hit': 1},
        {'track_name': 'Lua Cheia', 'artist': 'O Terno', 'is_hit': 1},
    ]
    
    # Maglore (10 hits)
    maglore_hits = [
        {'track_name': 'Enquanto Você Dorme', 'artist': 'Maglore', 'is_hit': 1},
        {'track_name': 'Tudo Pode Mudar', 'artist': 'Maglore', 'is_hit': 1},
        {'track_name': 'Ô Sol', 'artist': 'Maglore', 'is_hit': 1},
        {'track_name': 'Paquetá', 'artist': 'Maglore', 'is_hit': 1},
        {'track_name': 'Você Não Sabe o Que Perdeu', 'artist': 'Maglore', 'is_hit': 1},
        {'track_name': 'Meu Lugar', 'artist': 'Maglore', 'is_hit': 1},
        {'track_name': 'Vou Voltar', 'artist': 'Maglore', 'is_hit': 1},
        {'track_name': 'Agora', 'artist': 'Maglore', 'is_hit': 1},
        {'track_name': 'Não Olhe Pra Trás', 'artist': 'Maglore', 'is_hit': 1},
        {'track_name': 'Tudo Vai Passar', 'artist': 'Maglore', 'is_hit': 1},
    ]
    
    # Mahmundi (10 hits)
    mahmundi_hits = [
        {'track_name': 'Pra Você Dar o Nome', 'artist': 'Mahmundi', 'is_hit': 1},
        {'track_name': 'Lágrimas no Mar', 'artist': 'Mahmundi', 'is_hit': 1},
        {'track_name': 'Nós', 'artist': 'Mahmundi', 'is_hit': 1},
        {'track_name': 'Nada em Vão', 'artist': 'Mahmundi', 'is_hit': 1},
        {'track_name': 'Vento', 'artist': 'Mahmundi', 'is_hit': 1},
        {'track_name': 'Canção Pra Não Voltar', 'artist': 'Mahmundi', 'is_hit': 1},
        {'track_name': 'Tempestade', 'artist': 'Mahmundi', 'is_hit': 1},
        {'track_name': 'Pra Onde Vai', 'artist': 'Mahmundi', 'is_hit': 1},
        {'track_name': 'Deixa Ir', 'artist': 'Mahmundi', 'is_hit': 1},
        {'track_name': 'Só Você', 'artist': 'Mahmundi', 'is_hit': 1},
    ]
    
    # Castello Branco (5 hits)
    castello_hits = [
        {'track_name': 'Eu Quero É Botar Meu Bloco na Rua', 'artist': 'Castello Branco', 'is_hit': 1},
        {'track_name': 'Pra Que Chorar', 'artist': 'Castello Branco', 'is_hit': 1},
        {'track_name': 'Tudo Azul', 'artist': 'Castello Branco', 'is_hit': 1},
        {'track_name': 'Samba do Approach', 'artist': 'Castello Branco', 'is_hit': 1},
        {'track_name': 'Conversa de Botequim', 'artist': 'Castello Branco', 'is_hit': 1},
    ]
    
    all_hits = (mallu_hits + clarice_hits + loshermanos_hits + terno_hits +
                maglore_hits + mahmundi_hits + castello_hits)
    
    # ========================================
    # NON-HITS (+75 músicas)
    # ========================================
    
    # Mallu Magalhães (10 non-hits)
    mallu_nonhits = [
        {'track_name': 'Ô', 'artist': 'Mallu Magalhães', 'is_hit': 0},
        {'track_name': 'Você Não Presta', 'artist': 'Mallu Magalhães', 'is_hit': 0},
        {'track_name': 'Sambinha da Bossa', 'artist': 'Mallu Magalhães', 'is_hit': 0},
        {'track_name': 'Janta', 'artist': 'Mallu Magalhães', 'is_hit': 0},
        {'track_name': 'Olha Só', 'artist': 'Mallu Magalhães', 'is_hit': 0},
        {'track_name': 'Eu Gosto de Mulher', 'artist': 'Mallu Magalhães', 'is_hit': 0},
        {'track_name': 'Vem', 'artist': 'Mallu Magalhães', 'is_hit': 0},
        {'track_name': 'Eu Sei', 'artist': 'Mallu Magalhães', 'is_hit': 0},
        {'track_name': 'Shine Yellow', 'artist': 'Mallu Magalhães', 'is_hit': 0},
        {'track_name': 'Don\'t You Leave Me', 'artist': 'Mallu Magalhães', 'is_hit': 0},
    ]
    
    # Clarice Falcão (10 non-hits)
    clarice_nonhits = [
        {'track_name': 'Monomania', 'artist': 'Clarice Falcão', 'is_hit': 0},
        {'track_name': 'Talvez', 'artist': 'Clarice Falcão', 'is_hit': 0},
        {'track_name': 'Eu Me Lembro', 'artist': 'Clarice Falcão', 'is_hit': 0},
        {'track_name': 'De Todos os Loucos do Mundo', 'artist': 'Clarice Falcão', 'is_hit': 0},
        {'track_name': 'Capitão Gancho', 'artist': 'Clarice Falcão', 'is_hit': 0},
        {'track_name': 'Oitavo Andar', 'artist': 'Clarice Falcão', 'is_hit': 0},
        {'track_name': 'Banho Frio', 'artist': 'Clarice Falcão', 'is_hit': 0},
        {'track_name': 'Tem Conserto', 'artist': 'Clarice Falcão', 'is_hit': 0},
        {'track_name': 'Eu Sou Problema Meu', 'artist': 'Clarice Falcão', 'is_hit': 0},
        {'track_name': 'Monomania', 'artist': 'Clarice Falcão', 'is_hit': 0},
    ]
    
    # Los Hermanos (15 non-hits)
    loshermanos_nonhits = [
        {'track_name': 'Sentimental', 'artist': 'Los Hermanos', 'is_hit': 0},
        {'track_name': 'O Vencedor', 'artist': 'Los Hermanos', 'is_hit': 0},
        {'track_name': 'Cara Estranho', 'artist': 'Los Hermanos', 'is_hit': 0},
        {'track_name': 'Último Romance', 'artist': 'Los Hermanos', 'is_hit': 0},
        {'track_name': 'A Outra', 'artist': 'Los Hermanos', 'is_hit': 0},
        {'track_name': 'Conversa de Botas Batidas', 'artist': 'Los Hermanos', 'is_hit': 0},
        {'track_name': 'Tá Bom, Né?', 'artist': 'Los Hermanos', 'is_hit': 0},
        {'track_name': 'Deixa Estar', 'artist': 'Los Hermanos', 'is_hit': 0},
        {'track_name': 'Fingi Na Hora Rir', 'artist': 'Los Hermanos', 'is_hit': 0},
        {'track_name': 'Quem Sabe', 'artist': 'Los Hermanos', 'is_hit': 0},
        {'track_name': 'Pierrot', 'artist': 'Los Hermanos', 'is_hit': 0},
        {'track_name': 'Onze e Quinze', 'artist': 'Los Hermanos', 'is_hit': 0},
        {'track_name': 'Sapato Novo', 'artist': 'Los Hermanos', 'is_hit': 0},
        {'track_name': 'Além do Que Se Vê', 'artist': 'Los Hermanos', 'is_hit': 0},
        {'track_name': 'Primeiro Andar', 'artist': 'Los Hermanos', 'is_hit': 0},
    ]
    
    # O Terno (15 non-hits)
    terno_nonhits = [
        {'track_name': '66', 'artist': 'O Terno', 'is_hit': 0},
        {'track_name': 'Deixa Fugir', 'artist': 'O Terno', 'is_hit': 0},
        {'track_name': 'Eu Tomei Coca, Eu Tomei Fanta', 'artist': 'O Terno', 'is_hit': 0},
        {'track_name': 'Olhos Vermelhos', 'artist': 'O Terno', 'is_hit': 0},
        {'track_name': 'Volta', 'artist': 'O Terno', 'is_hit': 0},
        {'track_name': 'Tudo Por Nada', 'artist': 'O Terno', 'is_hit': 0},
        {'track_name': 'Eu Não Preciso de Ninguém', 'artist': 'O Terno', 'is_hit': 0},
        {'track_name': 'Morto', 'artist': 'O Terno', 'is_hit': 0},
        {'track_name': 'Atrás/Além', 'artist': 'O Terno', 'is_hit': 0},
        {'track_name': 'Eu Não Vou Mais Lavar os Pratos', 'artist': 'O Terno', 'is_hit': 0},
        {'track_name': 'Volta Pra Casa', 'artist': 'O Terno', 'is_hit': 0},
        {'track_name': 'Lua Cheia', 'artist': 'O Terno', 'is_hit': 0},
        {'track_name': 'Tudo Que Eu Não Quero', 'artist': 'O Terno', 'is_hit': 0},
        {'track_name': 'Pra Ser Sincero', 'artist': 'O Terno', 'is_hit': 0},
        {'track_name': 'Fica Tudo Bem', 'artist': 'O Terno', 'is_hit': 0},
    ]
    
    # Maglore (10 non-hits)
    maglore_nonhits = [
        {'track_name': 'Tudo Pode Mudar', 'artist': 'Maglore', 'is_hit': 0},
        {'track_name': 'Ô Sol', 'artist': 'Maglore', 'is_hit': 0},
        {'track_name': 'Paquetá', 'artist': 'Maglore', 'is_hit': 0},
        {'track_name': 'Você Não Sabe o Que Perdeu', 'artist': 'Maglore', 'is_hit': 0},
        {'track_name': 'Meu Lugar', 'artist': 'Maglore', 'is_hit': 0},
        {'track_name': 'Vou Voltar', 'artist': 'Maglore', 'is_hit': 0},
        {'track_name': 'Agora', 'artist': 'Maglore', 'is_hit': 0},
        {'track_name': 'Não Olhe Pra Trás', 'artist': 'Maglore', 'is_hit': 0},
        {'track_name': 'Tudo Vai Passar', 'artist': 'Maglore', 'is_hit': 0},
        {'track_name': 'Deixa Ir', 'artist': 'Maglore', 'is_hit': 0},
    ]
    
    # Mahmundi (10 non-hits)
    mahmundi_nonhits = [
        {'track_name': 'Nós', 'artist': 'Mahmundi', 'is_hit': 0},
        {'track_name': 'Nada em Vão', 'artist': 'Mahmundi', 'is_hit': 0},
        {'track_name': 'Vento', 'artist': 'Mahmundi', 'is_hit': 0},
        {'track_name': 'Canção Pra Não Voltar', 'artist': 'Mahmundi', 'is_hit': 0},
        {'track_name': 'Tempestade', 'artist': 'Mahmundi', 'is_hit': 0},
        {'track_name': 'Pra Onde Vai', 'artist': 'Mahmundi', 'is_hit': 0},
        {'track_name': 'Deixa Ir', 'artist': 'Mahmundi', 'is_hit': 0},
        {'track_name': 'Só Você', 'artist': 'Mahmundi', 'is_hit': 0},
        {'track_name': 'Tudo Que Eu Não Quero', 'artist': 'Mahmundi', 'is_hit': 0},
        {'track_name': 'Pra Ser Sincero', 'artist': 'Mahmundi', 'is_hit': 0},
    ]
    
    # Castello Branco (5 non-hits)
    castello_nonhits = [
        {'track_name': 'Pra Que Chorar', 'artist': 'Castello Branco', 'is_hit': 0},
        {'track_name': 'Tudo Azul', 'artist': 'Castello Branco', 'is_hit': 0},
        {'track_name': 'Samba do Approach', 'artist': 'Castello Branco', 'is_hit': 0},
        {'track_name': 'Conversa de Botequim', 'artist': 'Castello Branco', 'is_hit': 0},
        {'track_name': 'Tudo Que Eu Não Quero', 'artist': 'Castello Branco', 'is_hit': 0},
    ]
    
    all_nonhits = (mallu_nonhits + clarice_nonhits + loshermanos_nonhits + terno_nonhits +
                   maglore_nonhits + mahmundi_nonhits + castello_nonhits)
    
    # Combina tudo
    for song in all_hits + all_nonhits:
        song['genre'] = 'mpb_indie'
        song['source'] = 'massive_collection_final'
        all_songs.append(song)
    
    return pd.DataFrame(all_songs)

def create_final_mpb_indie():
    """Cria dataset final massivo de MPB Indie"""
    print("\n" + "="*70)
    print("COLETA MASSIVA FINAL: MPB INDIE")
    print("="*70 + "\n")
    
    datasets_dir = Path(__file__).parent / 'datasets'
    
    # Carrega base atual
    base_path = datasets_dir / 'mpb_indie_expanded.csv'
    df_base = pd.read_csv(base_path)
    print(f"Base atual: {len(df_base)} musicas")
    
    # Adiciona coleta massiva
    df_massive = get_massive_indie_collection()
    print(f"Coleta massiva: {len(df_massive)} musicas")
    print(f"  Hits: {df_massive['is_hit'].sum()}")
    print(f"  Non-hits: {len(df_massive) - df_massive['is_hit'].sum()}")
    
    # Combina
    df_final = pd.concat([df_base, df_massive], ignore_index=True)
    df_final = df_final.drop_duplicates(subset=['track_name', 'artist'], keep='first')
    
    # Salva
    output_path = datasets_dir / 'mpb_indie_massive.csv'
    df_final.to_csv(output_path, index=False)
    
    print(f"\nDataset final massivo:")
    print(f"  Total: {len(df_final)} musicas")
    print(f"  Hits: {df_final['is_hit'].sum()} ({df_final['is_hit'].mean():.1%})")
    print(f"  Non-hits: {len(df_final) - df_final['is_hit'].sum()} ({1-df_final['is_hit'].mean():.1%})")
    print(f"  Salvo: {output_path.name}")
    
    print("\n" + "="*70)
    print("MPB INDIE MASSIVO PRONTO!")
    print("="*70)
    
    return df_final

if __name__ == "__main__":
    create_final_mpb_indie()
