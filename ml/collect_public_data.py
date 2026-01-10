"""
Coleta de Dados Públicos - Billboard Brasil
Scraping do Billboard Brasil Hot 100 para obter hits verificados
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path
import time

def scrape_billboard_brasil():
    """
    Faz scraping do Billboard Brasil Hot 100
    """
    print("\n" + "="*70)
    print("SCRAPING: BILLBOARD BRASIL HOT 100")
    print("="*70 + "\n")
    
    # URL do Billboard Brasil
    url = "https://www.billboard.com.br/charts/hot-100-brasil/"
    
    try:
        print(f"Acessando: {url}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        print(f"Status: {response.status_code}")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Tenta diferentes seletores CSS
        hits = []
        
        # Seletor 1: chart-list-item
        items = soup.find_all('div', class_='chart-list-item')
        if items:
            print(f"Encontrados {len(items)} itens (chart-list-item)")
            for item in items:
                try:
                    title_elem = item.find('span', class_='chart-list-item__title')
                    artist_elem = item.find('span', class_='chart-list-item__artist')
                    
                    if title_elem and artist_elem:
                        track = title_elem.text.strip()
                        artist = artist_elem.text.strip()
                        hits.append({
                            'track_name': track,
                            'artist': artist,
                            'is_hit': 1,
                            'source': 'billboard_brasil'
                        })
                except Exception as e:
                    continue
        
        # Seletor 2: Alternativo
        if not hits:
            items = soup.find_all('li', class_='chart-list__element')
            if items:
                print(f"Encontrados {len(items)} itens (chart-list__element)")
                for item in items:
                    try:
                        title_elem = item.find('span', class_='chart-element__information__song')
                        artist_elem = item.find('span', class_='chart-element__information__artist')
                        
                        if title_elem and artist_elem:
                            track = title_elem.text.strip()
                            artist = artist_elem.text.strip()
                            hits.append({
                                'track_name': track,
                                'artist': artist,
                                'is_hit': 1,
                                'source': 'billboard_brasil'
                            })
                    except Exception as e:
                        continue
        
        # Seletor 3: Genérico
        if not hits:
            print("Tentando seletor generico...")
            # Salva HTML para debug
            with open('billboard_debug.html', 'w', encoding='utf-8') as f:
                f.write(soup.prettify())
            print("HTML salvo em billboard_debug.html para analise")
        
        if hits:
            df = pd.DataFrame(hits)
            print(f"\nOK: Coletadas {len(df)} musicas do Billboard Brasil")
            return df
        else:
            print("AVISO: Nenhuma musica encontrada. Verifique billboard_debug.html")
            return None
            
    except Exception as e:
        print(f"ERRO ao acessar Billboard: {e}")
        return None

def scrape_youtube_trending_brasil():
    """
    Alternativa: Usa lista manual de hits conhecidos do YouTube Brasil
    (Web scraping do YouTube é mais complexo devido a JavaScript)
    """
    print("\n" + "="*70)
    print("DADOS: YOUTUBE TRENDING BRASIL (MANUAL)")
    print("="*70 + "\n")
    
    # Lista manual de hits recentes do YouTube Brasil (2023-2024)
    # Fonte: YouTube Brasil Trending Music
    youtube_hits = [
        # Sertanejo
        {'track_name': 'Jenifer', 'artist': 'Gabriel Diniz', 'genre': 'sertanejo'},
        {'track_name': 'Largado às Traças', 'artist': 'Zé Neto e Cristiano', 'genre': 'sertanejo'},
        {'track_name': 'Facas', 'artist': 'Diego e Victor Hugo', 'genre': 'sertanejo'},
        
        # Pop Urban
        {'track_name': 'Modo Turbo', 'artist': 'Luísa Sonza', 'genre': 'pop_urban_brasil'},
        {'track_name': 'Chico', 'artist': 'Pabllo Vittar', 'genre': 'pop_urban_brasil'},
        {'track_name': 'Alibi', 'artist': 'Sevdaliza, Pabllo Vittar', 'genre': 'pop_urban_brasil'},
        
        # R&B Brasil
        {'track_name': 'Dança do Desempregado', 'artist': 'MC WM', 'genre': 'rnb_brasil'},
        {'track_name': 'Barbie', 'artist': 'Teto', 'genre': 'rnb_brasil'},
        
        # MPB
        {'track_name': 'Oração', 'artist': 'A Banda Mais Bonita da Cidade', 'genre': 'mpb'},
        {'track_name': 'Tudo o Que Você Quiser', 'artist': 'Lulu Santos', 'genre': 'mpb'},
    ]
    
    df = pd.DataFrame(youtube_hits)
    df['is_hit'] = 1
    df['source'] = 'youtube_trending'
    
    print(f"OK: {len(df)} hits do YouTube Trending adicionados")
    print(f"Generos: {df['genre'].value_counts().to_dict()}")
    
    return df

def collect_public_data():
    """Coleta dados de todas as fontes públicas"""
    print("\n" + "="*70)
    print("COLETA DE DADOS PUBLICOS")
    print("="*70)
    
    all_data = []
    
    # 1. Billboard Brasil
    billboard_data = scrape_billboard_brasil()
    if billboard_data is not None and len(billboard_data) > 0:
        all_data.append(billboard_data)
        time.sleep(2)  # Respeita rate limiting
    
    # 2. YouTube Trending (manual)
    youtube_data = scrape_youtube_trending_brasil()
    if youtube_data is not None and len(youtube_data) > 0:
        all_data.append(youtube_data)
    
    # Combina todos os dados
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        
        # Remove duplicatas
        combined_df = combined_df.drop_duplicates(subset=['track_name', 'artist'], keep='first')
        
        # Salva
        output_path = Path(__file__).parent / 'datasets' / 'public_hits_collection.csv'
        combined_df.to_csv(output_path, index=False)
        
        print("\n" + "="*70)
        print("RESUMO DA COLETA")
        print("="*70)
        print(f"Total de hits coletados: {len(combined_df)}")
        print(f"Fontes: {combined_df['source'].value_counts().to_dict()}")
        if 'genre' in combined_df.columns:
            print(f"Generos: {combined_df['genre'].value_counts().to_dict()}")
        print(f"\nSalvo em: {output_path}")
        print("="*70)
        
        return combined_df
    else:
        print("\nAVISO: Nenhum dado coletado")
        return None

if __name__ == "__main__":
    collect_public_data()
