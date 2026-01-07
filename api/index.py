import os
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import traceback

# Add the project root to sys.path so we can import modules from 'backend'
# Path structure on Vercel: /var/task/
# Our files: /var/task/api/index.py, /var/task/backend/audio_analyzer.py, etc.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.audio_analyzer import AudioAnalyzer
from backend.hit_predictor import HitPredictor

app = Flask(__name__)
CORS(app)

# Use /tmp for uploads in serverless environments
UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'ogg', 'flac', 'm4a'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Hit Predictor API is running on Vercel'})

@app.route('/analyze', methods=['POST'])
def analyze_audio():
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'Nenhum arquivo de áudio enviado'}), 400
        
        file = request.files['audio']
        if file.filename == '':
            return jsonify({'error': 'Arquivo sem nome'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                'error': f'Formato não suportado. Use: {", ".join(ALLOWED_EXTENSIONS)}'
            }), 400
        
        genre = request.form.get('genre', None)
        if genre and genre.lower() == 'generic':
            genre = None
        
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            analyzer = AudioAnalyzer(filepath)
            features = analyzer.analyze_all()
            
            predictor = HitPredictor(genre=genre)
            prediction = predictor.predict(features)
            
            result = {
                'success': True,
                'filename': filename,
                'features': features,
                'prediction': prediction
            }
            return jsonify(result)
        
        finally:
            if os.path.exists(filepath):
                os.remove(filepath)
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({
            'error': 'Erro ao processar áudio',
            'details': str(e)
        }), 500

@app.route('/genres', methods=['GET'])
def get_genres():
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

# Required for Vercel
handler = app
