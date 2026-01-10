import os
import sys

# Corrige encoding do terminal no Windows para evitar erros com emojis/unicode
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

import gc
import traceback
import time

# =================================================================
# CONFIGURAÇÕES DE AMBIENTE (DEVEM VIR ANTES DE QUALQUER OUTRO IMPORT)
# =================================================================
# Desabilita JIT do Numba para evitar crashes no Python 3.14 / Windows
os.environ['NUMBA_DISABLE_JIT'] = '1'
# Limita threads para economizar RAM e evitar conflitos em processamento paralelo
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['VECLIB_MAXIMUM_THREADS'] = '1'
os.environ['NUMEXPR_NUM_THREADS'] = '1'
# =================================================================

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
if getattr(sys, 'frozen', False):
    # Running in a bundle (.exe)
    project_root = sys._MEIPASS
    # Adiciona o diretório temporário ao PATH para que o librosa encontre o ffmpeg.exe
    os.environ["PATH"] += os.pathsep + project_root
    # No EXE, o frontend fica dentro da raiz do bundle
    static_dir = os.path.join(project_root, 'frontend')
else:
    # Running in normal Python environment
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    os.environ["PATH"] += os.pathsep + project_root
    static_dir = os.path.join(project_root, 'frontend')
    
    # Adiciona a raiz ao sys.path para que imports de 'backend' funcionem
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

# Imports locais do projeto (agora que o path está corrigido)
try:
    from backend.audio_analyzer import AudioAnalyzer
    from backend.hit_predictor import HitPredictor
    print("[INIT] Modulos internos carregados com sucesso")
except ImportError as e:
    print(f"[ERROR] Erro ao carregar modulos internos: {e}")
    # Tenta import direto se estiver dentro da pasta backend
    try:
        from audio_analyzer import AudioAnalyzer
        from hit_predictor import HitPredictor
        print("[INIT] Modulos internos carregados (import direto)")
    except ImportError:
        print("[ERROR] Falha critica no carregamento dos modulos")

print(f"DEBUG: Modo Executável: {getattr(sys, 'frozen', False)}")
print(f"DEBUG: Diretório Base: {project_root}")
print(f"DEBUG: Pasta do Frontend: {static_dir}")

import logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app)


# Configurações
UPLOAD_FOLDER = os.path.join(project_root, 'backend', 'uploads')
def get_hit_averages_by_genre(genre_id):
    """Retorna médias das features dos hits para um gênero específico"""
    import pandas as pd
    
    # Mapeia genre_id para arquivo de dataset
    # Cada gênero tem seu próprio dataset específico
    mpb_dataset = os.path.join(project_root, 'ml', 'datasets', 'kaggle_mpb_ml.csv')
    rnb_dataset = os.path.join(project_root, 'ml', 'datasets', 'kaggle_rnb_ml.csv')
    pop_urban_dataset = os.path.join(project_root, 'ml', 'datasets', 'kaggle_pop_urban_brasil_ml.csv')
    sertanejo_dataset = os.path.join(project_root, 'ml', 'datasets', 'kaggle_sertanejo_ml.csv')
    forro_dataset = os.path.join(project_root, 'ml', 'datasets', 'kaggle_forro_ml.csv')
    pagode_dataset = os.path.join(project_root, 'ml', 'datasets', 'kaggle_pagode_ml.csv')
    samba_dataset = os.path.join(project_root, 'ml', 'datasets', 'kaggle_samba_ml.csv')
    
    genre_files = {
        'mpb': mpb_dataset,
        'mpb_rock': mpb_dataset,
        'mpb_indie': mpb_dataset,
        'rnb_brasil': rnb_dataset,
        'rnb_trap': rnb_dataset,
        'rnb_pop': rnb_dataset,
        'pop_urban_brasil': pop_urban_dataset,
        'sertanejo': sertanejo_dataset,
        'pagode': pagode_dataset,
        'samba': samba_dataset,
        'forro': forro_dataset,
        'brazil': pop_urban_dataset,
        'generic': None
    }
    
    file_path = genre_files.get(genre_id)
    if not file_path or not os.path.exists(file_path):
        print(f"    [WARNING] Dataset não encontrado para gênero: {genre_id}")
        return None
    
    try:
        df = pd.read_csv(file_path)
        hits = df[df['is_hit'] == 1]
        
        if len(hits) == 0:
            print(f"    [WARNING] Nenhum hit encontrado no dataset: {genre_id}")
            return None
        
        features = ['bpm', 'energy', 'danceability', 'valence', 
                    'acousticness', 'instrumentalness', 'liveness', 
                    'speechiness', 'loudness']
        
        averages = {}
        for feature in features:
            if feature in hits.columns:
                averages[feature] = float(hits[feature].mean())
        
        print(f"    [DEBUG] Médias calculadas para {genre_id}: {len(averages)} features")
        return averages
        
    except Exception as e:
        print(f"    [ERROR] Erro ao calcular médias para {genre_id}: {e}")
        return None

ALLOWED_EXTENSIONS = {'mp3', 'wav', 'ogg', 'flac', 'm4a'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

# Cria pasta de uploads se não existir
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

def allowed_file(filename):
    """Verifica se a extensão do arquivo é permitida"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.before_request
def log_request_info():
    print(f"\n>>> [HTTP] {request.method} {request.path}")
    if request.path.startswith('/api/'):
        print(f"    Headers: {dict(request.headers)}")

@app.after_request
def log_response_info(response):
    print(f"<<< [HTTP] {request.method} {request.path} - Status: {response.status_code}")
    return response

@app.route('/api/ping', methods=['GET'])
def ping():
    return jsonify({'pong': True, 'static_dir': static_dir, 'upload_dir': UPLOAD_FOLDER})

@app.route('/api/health', methods=['GET'])
def health_check():
    """Endpoint de health check"""
    return jsonify({'status': 'healthy', 'message': 'Hit Predictor API is running'})

@app.route('/api/analyze', methods=['POST'])
def analyze_audio():
    """Endpoint principal para análise de áudio"""
    try:
        # Verifica se há arquivo na requisição
        if 'audio' not in request.files:
            return jsonify({'error': 'Nenhum arquivo de áudio enviado'}), 400
        
        file = request.files['audio']
        
        # Verifica se o arquivo tem nome
        if file.filename == '':
            return jsonify({'error': 'Arquivo sem nome'}), 400
        
        # Verifica extensão
        if not allowed_file(file.filename):
            return jsonify({
                'error': f'Formato não suportado. Use: {", ".join(ALLOWED_EXTENSIONS)}'
            }), 400
        
        # Pega gêneros selecionados (pode ser um ou vários)
        requested_genres = request.form.getlist('genres[]')
        if not requested_genres:
            # Fallback para o campo antigo 'genre' se o novo não existir
            old_genre = request.form.get('genre', 'generic')
            requested_genres = [old_genre]
            
        # Salva arquivo temporariamente com nome seguro e único
        base_filename = secure_filename(file.filename)
        if not base_filename:
            base_filename = f"upload_{int(time.time())}.mp3"
        
        filename = f"{int(time.time())}_{base_filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        print(f">>> [UPLOAD] Salvando arquivo em: {filepath}")
        file.save(filepath)
        
        # Garante que o arquivo foi escrito (pequeno delay para o Windows)
        time.sleep(0.3)
        
        if not os.path.exists(filepath):
            return jsonify({'error': 'Falha ao salvar arquivo no servidor'}), 500

        try:
            # Analisa áudio (extração de features é feita só uma vez)
            print(f">>> [IA] Iniciando extração de features: {filename}")
            
            analyzer = AudioAnalyzer(filepath)            # Análise
            features = analyzer.analyze_all()
            
            print(f"\n[DEBUG] FEATURES EXTRAIDAS EM TEMPO REAL:")
            print(f"File: {file.filename}")
            for k, v in features.items():
                print(f"  {k}: {v}")
            
            # Log das features extraídas para o terminal
            print(f"    [RESULTS] {file.filename}: BPM={features['bpm']:.1f}, Energy={features['energy']:.2f}, Loudness={features['loudness']:.1f}dB")
            
            # Predições
            predictions = {}
            for genre_id in requested_genres:
                actual_genre = None if genre_id == 'generic' else genre_id
                predictor = HitPredictor(genre=actual_genre)
                prediction = predictor.predict(features)
                
                # Adiciona médias dos hits para comparação
                hit_averages = get_hit_averages_by_genre(genre_id)
                prediction['hit_averages'] = hit_averages
                
                predictions[genre_id] = prediction
                print(f"    - Score para {genre_id}: {prediction['hit_score']}")
            
            return jsonify({
                'success': True,
                'filename': filename,
                'features': features,
                'predictions': predictions # Novo formato: mapa de gênero -> predição
            })
        except Exception as analysis_err:
            print(f"❌ ERRO Durante Análise IA: {str(analysis_err)}")
            traceback.print_exc()
            return jsonify({
                'error': f'Falha na análise da música: {str(analysis_err)}',
                'details': traceback.format_exc()
            }), 500
        
        finally:
            # Limpeza agressiva de memória antes de tentar deletar o arquivo
            gc.collect()
            
            # Remove arquivo temporário (com segurança para Windows)
            if os.path.exists(filepath):
                try:
                    os.remove(filepath)
                except Exception as cleanup_error:
                    print(f"⚠️ Aviso: Não foi possível deletar arquivo temporário: {cleanup_error}")
            
            gc.collect()
    
    except Exception as e:
        print(f"❌ ERRO na Rota Analyze: {str(e)}")
        traceback.print_exc()
        return jsonify({
            'error': f'Erro ao processar áudio: {str(e)}',
            'details': traceback.format_exc()
        }), 500

@app.route('/api/supported-formats', methods=['GET'])
def get_supported_formats():
    """Retorna formatos de áudio suportados"""
    return jsonify({
        'formats': list(ALLOWED_EXTENSIONS),
        'max_size_mb': MAX_FILE_SIZE / (1024 * 1024)
    })

@app.route('/api/genres', methods=['GET'])
def get_genres():
    """Retorna gêneros musicais disponíveis com modelos ML"""
    return jsonify({
        'genres': [
            # R&B Brasil - Subcategorias
            {'id': 'rnb_trap', 'name': 'R&B Trap', 'has_ml_model': True, 'accuracy': '78%'},
            {'id': 'rnb_pop', 'name': 'R&B Pop', 'has_ml_model': True, 'accuracy': '75%'},
            
            # MPB - Subcategorias
            {'id': 'mpb_rock', 'name': 'MPB Rock', 'has_ml_model': True, 'accuracy': '65%'},
            {'id': 'mpb_indie', 'name': 'MPB Indie', 'has_ml_model': True, 'accuracy': '65-70%'},
            
            # Outros gêneros
            {'id': 'sertanejo', 'name': 'Sertanejo', 'has_ml_model': True, 'accuracy': '71%'},
            {'id': 'pagode', 'name': 'Pagode', 'has_ml_model': True, 'accuracy': '63%'},
            {'id': 'samba', 'name': 'Samba', 'has_ml_model': True, 'accuracy': '71%'},
            {'id': 'forro', 'name': 'Forró', 'has_ml_model': True},
            {'id': 'pop_urban_brasil', 'name': 'Pop/Urban Brasil', 'has_ml_model': True, 'accuracy': '63%'}
        ]
    })


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handler para arquivos muito grandes"""
    return jsonify({
        'error': 'Arquivo muito grande',
        'max_size_mb': MAX_FILE_SIZE / (1024 * 1024)
    }), 413

# Verificação de segurança da pasta frontend
if not os.path.exists(os.path.join(static_dir, 'index.html')):
    print(f"!!! ERRO CRITICO: 'index.html' nao encontrado em: {static_dir}")
else:
    print(f"[OK] 'index.html' verificado com sucesso em: {static_dir}")

@app.after_request
def log_response_info(response):
    print(f">>> [HTTP] {request.method} {request.path} - Status: {response.status_code}")
    return response

@app.errorhandler(Exception)
def handle_exception(e):
    """Captura QUALQUER erro não tratado e retorna JSON"""
    print(f"!!! ERRO GLOBAL: {str(e)}")
    traceback.print_exc()
    return jsonify({
        'error': f'Erro interno no servidor: {str(e)}',
        'traceback': traceback.format_exc()
    }), 500

@app.route('/')
def index():
    """Serve o index.html principal"""
    return send_from_directory(static_dir, 'index.html')

@app.route('/api/<path:subpath>', methods=['GET', 'POST', 'OPTIONS'])
def api_404(subpath):
    """Garante que qualquer erro em /api retorne JSON, não HTML"""
    return jsonify({'error': f'Rota da API não encontrada: /api/{subpath}'}), 404

@app.route('/<path:path>')
def static_proxy(path):
    """Serve arquivos estáticos (css, js, etc)"""
    full_path = os.path.join(static_dir, path)
    if os.path.isfile(full_path):
        return send_from_directory(static_dir, path)
    return send_from_directory(static_dir, 'index.html')

def get_hit_averages_by_genre(genre_id):
    """Retorna médias das features dos hits para o gênero"""
    if genre_id == 'brazil': 
        genre_id = 'pop_urban_brasil'
        
    features = ['bpm', 'energy', 'danceability', 'valence', 
                'acousticness', 'instrumentalness', 'liveness', 
                'speechiness', 'loudness']
    
    # Reutiliza lógica de arquivo do main
    import sys
    if getattr(sys, 'frozen', False):
        project_root = sys._MEIPASS
    else:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
    ml_dir = os.path.join(project_root, 'ml', 'datasets')
    
    # Mapeamento simples
    dataset_map = {
        'mpb': 'kaggle_mpb_ml.csv',
        'rnb_brasil': 'kaggle_rnb_ml.csv',
        'pop_urban_brasil': 'kaggle_pop_urban_brasil_ml.csv',
        'sertanejo': 'kaggle_sertanejo_ml.csv',
        'pagode': 'kaggle_pagode_ml.csv',
        'samba': 'kaggle_samba_ml.csv',
        'forro': 'kaggle_forro_ml.csv'
    }
    
    filename = dataset_map.get(genre_id)
    if not filename: return None
    
    path = os.path.join(ml_dir, filename)
    if not os.path.exists(path): return None
    
    try:
        import pandas as pd # Ensure pandas is imported
        df = pd.read_csv(path)
        hits = df[df['is_hit'] == 1]
        if hits.empty: return None
        
        avgs = {}
        for f in features:
            if f in hits.columns:
                avgs[f] = float(hits[f].mean())
        return avgs
    except:
        return None

if __name__ == '__main__':
    PORT = 5002
    print(f"\n==========================================")
    print(f"Hit Predictor rodando em: http://localhost:{PORT}")
    print(f"==========================================\n")
    
    import webbrowser
    # Atrasar um pouco para o usuário ver as mensagens de boot
    time.sleep(1)
    webbrowser.open(f'http://localhost:{PORT}')
    
    # Rodar com logger para ver erros de rede/conexão
    # IMPORTANTE: use_reloader=True para recarregar mudanças automaticamente
    app.run(debug=True, host='0.0.0.0', port=PORT, use_reloader=True)
