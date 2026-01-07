from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import traceback
from audio_analyzer import AudioAnalyzer
from hit_predictor import HitPredictor

app = Flask(__name__)
CORS(app)

# Configurações
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'ogg', 'flac', 'm4a'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

# Cria pasta de uploads se não existir
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

def allowed_file(filename):
    """Verifica se a extensão do arquivo é permitida"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de health check"""
    return jsonify({'status': 'healthy', 'message': 'Hit Predictor API is running'})

@app.route('/analyze', methods=['POST'])
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
        
        # Pega gênero opcional
        genre = request.form.get('genre', None)
        if genre and genre.lower() == 'generic':
            genre = None  # Usa heurísticas genéricas
        
        # Salva arquivo temporariamente
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Analisa áudio
            print(f"Analisando arquivo: {filename}")
            if genre:
                print(f"Genero selecionado: {genre}")
            analyzer = AudioAnalyzer(filepath)
            features = analyzer.analyze_all()
            
            # Prediz hit potential com gênero específico
            predictor = HitPredictor(genre=genre)
            prediction = predictor.predict(features)
            
            # Combina resultados
            result = {
                'success': True,
                'filename': filename,
                'features': features,
                'prediction': prediction
            }
            
            return jsonify(result)
        
        finally:
            # Remove arquivo temporário
            if os.path.exists(filepath):
                os.remove(filepath)
    
    except Exception as e:
        print(f"Erro ao processar áudio: {str(e)}")
        traceback.print_exc()
        return jsonify({
            'error': 'Erro ao processar áudio',
            'details': str(e)
        }), 500

@app.route('/supported-formats', methods=['GET'])
def get_supported_formats():
    """Retorna formatos de áudio suportados"""
    return jsonify({
        'formats': list(ALLOWED_EXTENSIONS),
        'max_size_mb': MAX_FILE_SIZE / (1024 * 1024)
    })

@app.route('/genres', methods=['GET'])
def get_genres():
    """Retorna gêneros musicais disponíveis com modelos ML"""
    return jsonify({
        'genres': [
            {'id': 'generic', 'name': 'Genérico (Heurísticas)', 'has_ml_model': False},
            {'id': 'mpb', 'name': 'MPB/Nova MPB', 'has_ml_model': True},
            {'id': 'rnb_brasil', 'name': 'R&B Brasil', 'has_ml_model': True},
            {'id': 'sertanejo', 'name': 'Sertanejo', 'has_ml_model': True},
            {'id': 'pagode', 'name': 'Pagode', 'has_ml_model': True},
            {'id': 'samba', 'name': 'Samba', 'has_ml_model': True},
            {'id': 'forro', 'name': 'Forró', 'has_ml_model': True},
            {'id': 'brazil', 'name': 'Pop/Urban Brasil', 'has_ml_model': True}
        ]
    })

@app.errorhandler(413)
def request_entity_too_large(error):
    """Handler para arquivos muito grandes"""
    return jsonify({
        'error': 'Arquivo muito grande',
        'max_size_mb': MAX_FILE_SIZE / (1024 * 1024)
    }), 413

if __name__ == '__main__':
    print("Hit Predictor API iniciando...")
    print(f"Pasta de uploads: {os.path.abspath(UPLOAD_FOLDER)}")
    print(f"Formatos suportados: {', '.join(ALLOWED_EXTENSIONS)}")
    print(f"Tamanho maximo: {MAX_FILE_SIZE / (1024 * 1024):.0f}MB")
    print("\nServidor rodando em http://localhost:5000\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
