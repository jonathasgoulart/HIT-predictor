# import numpy as np
# import joblib
import os
from pathlib import Path

class HitPredictor:
    """Modelo de predição baseado em heurísticas de características de hits"""
    
    # Features esperadas pelos modelos ML
    ML_FEATURES = ['bpm', 'energy', 'danceability', 'valence', 'acousticness', 
                   'instrumentalness', 'liveness', 'speechiness', 'loudness', 'duration_ms']
    
    # Cache global de modelos para evitar recarregamento pesado do disco (economia de RAM)
    _model_cache = {}
    
    def __init__(self, genre=None):
        """
        Inicializa preditor
        
        Args:
            genre: Gênero musical ('mpb', 'rnb_brasil', ou None para genérico)
        """
        self.genre = genre
        self.ml_model = None
        self.model_type = 'heuristic'  # 'heuristic' ou 'ml'
        
        # Tenta carregar modelo ML se gênero especificado
        if genre:
            self._load_ml_model(genre)
        
        # Ranges ideais baseados em análise de hits populares
        self.ideal_ranges = {
            'bpm': (110, 130),  # Sweet spot para pop/dance
            'energy': (0.5, 0.9),
            'loudness': (-8, -4),
            'danceability': (0.6, 0.95),
            'duration': (150, 240),  # 2.5 a 4 minutos
            'brightness': (1500, 3500),
            'dynamic_variation': (0.1, 0.4)
        }
        
        # Pesos para cada característica (total = 100)
        self.weights = {
            'bpm': 15,
            'energy': 20,
            'danceability': 25,
            'loudness': 10,
            'duration': 10,
            'brightness': 10,
            'dynamic_variation': 10
        }
    
    def _load_ml_model(self, genre):
        """Carrega modelo ML treinado para o gênero especificado"""
        try:
            # Caminho para diretório de modelos
            models_dir = Path(__file__).parent.parent / 'ml' / 'models'
            
            # Procura o modelo mais recente para o gênero
            pattern = f"{genre}_*.pkl"
            model_files = list(models_dir.glob(pattern))
            
            if model_files:
                # Pega o mais recente (último na lista ordenada)
                latest_model = sorted(model_files)[-1]
                model_path = str(latest_model)
                
                # Verifica se o modelo já está no cache
                if model_path in self._model_cache:
                    self.ml_model = self._model_cache[model_path]
                    print(f"Modelo ML recuperado do cache: {latest_model.name}")
                else:
                    import joblib
                    self.ml_model = joblib.load(latest_model)
                    self._model_cache[model_path] = self.ml_model
                    print(f"Modelo ML carregado do disco e cacheado: {latest_model.name}")
                
                self.model_type = 'ml'
            else:
                print(f"Nenhum modelo ML encontrado para genero '{genre}', usando heuristicas")
                
        except Exception as e:
            print(f"Erro ao carregar modelo ML: {e}")
            print("Usando heuristicas como fallback")
    
    def _prepare_ml_features(self, features):
        """Prepara features no formato esperado pelo modelo ML"""
        import numpy as np
        ml_input = []
        for feature_name in self.ML_FEATURES:
            # Mapeia nomes de features
            if feature_name == 'duration_ms':
                value = features.get('duration', 0) * 1000  # converte segundos para ms
            else:
                value = features.get(feature_name, 0)
            ml_input.append(value)
        return np.array([ml_input])
    
    def _predict_with_ml(self, features):
        """Faz predição usando modelo ML"""
        try:
            # Prepara features
            X = self._prepare_ml_features(features)
            
            # Predição
            prediction = self.ml_model.predict(X)[0]  # 0 ou 1
            probability = self.ml_model.predict_proba(X)[0][1]  # probabilidade de ser hit
            
            # Converte para score 0-100
            ml_score = int(probability * 100)
            
            return {
                'is_hit': bool(prediction),
                'hit_probability': probability,
                'ml_score': ml_score
            }
        except Exception as e:
            print(f"Erro na predicao ML: {e}")
            return None
    
    def normalize_score(self, value, ideal_min, ideal_max):
        """Normaliza score baseado em range ideal (0-1)"""
        if value < ideal_min:
            # Penaliza valores abaixo do ideal
            distance = ideal_min - value
            penalty = min(distance / ideal_min, 1)
            return 1 - penalty
        elif value > ideal_max:
            # Penaliza valores acima do ideal
            distance = value - ideal_max
            penalty = min(distance / ideal_max, 1)
            return 1 - penalty
        else:
            # Valor dentro do range ideal
            return 1.0
    
    def calculate_bpm_score(self, bpm):
        """Calcula score do BPM"""
        score = self.normalize_score(bpm, *self.ideal_ranges['bpm'])
        
        # Bonus para BPMs muito populares (120-128)
        if 120 <= bpm <= 128:
            score = min(score * 1.1, 1.0)
        
        return score
    
    def calculate_energy_score(self, energy):
        """Calcula score de energia"""
        return self.normalize_score(energy, *self.ideal_ranges['energy'])
    
    def calculate_danceability_score(self, danceability):
        """Calcula score de dançabilidade"""
        score = self.normalize_score(danceability, *self.ideal_ranges['danceability'])
        
        # Dançabilidade é crucial para hits modernos
        if danceability > 0.8:
            score = min(score * 1.15, 1.0)
        
        return score
    
    def calculate_loudness_score(self, loudness):
        """Calcula score de loudness"""
        return self.normalize_score(loudness, *self.ideal_ranges['loudness'])
    
    def calculate_duration_score(self, duration):
        """Calcula score de duração"""
        score = self.normalize_score(duration, *self.ideal_ranges['duration'])
        
        # Penaliza músicas muito longas (dificulta airplay)
        if duration > 300:  # 5 minutos
            score *= 0.7
        
        return score
    
    def calculate_brightness_score(self, brightness):
        """Calcula score de brightness (claridade espectral)"""
        return self.normalize_score(brightness, *self.ideal_ranges['brightness'])
    
    def calculate_variation_score(self, variation):
        """Calcula score de variação dinâmica"""
        return self.normalize_score(variation, *self.ideal_ranges['dynamic_variation'])
    
    def predict(self, features):
        """Calcula score total de hit potential (0-100)"""
        
        # Tenta usar modelo ML se disponível
        ml_result = None
        if self.ml_model:
            ml_result = self._predict_with_ml(features)
        
        # Calcula scores heurísticos (sempre, para comparação e fallback)
        scores = {}
        
        # Calcula score individual para cada característica
        if 'bpm' in features:
            scores['bpm'] = self.calculate_bpm_score(features['bpm'])
        
        if 'energy' in features:
            scores['energy'] = self.calculate_energy_score(features['energy'])
        
        if 'danceability' in features:
            scores['danceability'] = self.calculate_danceability_score(features['danceability'])
        
        if 'loudness' in features:
            scores['loudness'] = self.calculate_loudness_score(features['loudness'])
        
        if 'duration' in features:
            scores['duration'] = self.calculate_duration_score(features['duration'])
        
        if 'brightness' in features:
            scores['brightness'] = self.calculate_brightness_score(features['brightness'])
        
        if 'dynamic_variation' in features:
            scores['dynamic_variation'] = self.calculate_variation_score(features['dynamic_variation'])
        
        # Calcula score ponderado total (heurístico)
        total_score = 0
        for feature, score in scores.items():
            if feature in self.weights:
                total_score += score * self.weights[feature]
        
        heuristic_score = int(round(total_score))
        
        # Decide qual score usar
        if ml_result:
            # Usa score ML, mas mantém heurístico para comparação
            final_score = ml_result['ml_score']
            prediction_method = 'ml'
        else:
            final_score = heuristic_score
            prediction_method = 'heuristic'
        
        result = {
            'hit_score': final_score,
            'prediction_method': prediction_method,
            'individual_scores': {k: round(v * 100, 1) for k, v in scores.items()},
            'recommendations': self.generate_recommendations(features, scores)
        }
        
        # Adiciona informações ML se disponível
        if ml_result:
            result['ml_prediction'] = {
                'is_hit': ml_result['is_hit'],
                'probability': round(ml_result['hit_probability'] * 100, 1),
                'heuristic_score': heuristic_score  # Para comparação
            }
            result['genre'] = self.genre
        
        return result
    
    def generate_recommendations(self, features, scores):
        """Gera recomendações baseadas nos scores"""
        recommendations = []
        
        # BPM
        if 'bpm' in scores and scores['bpm'] < 0.7:
            bpm = features['bpm']
            if bpm < 110:
                recommendations.append({
                    'category': 'Tempo',
                    'message': f'BPM ({bpm:.0f}) está abaixo do ideal. Considere aumentar para 110-130 BPM.',
                    'priority': 'high'
                })
            elif bpm > 130:
                recommendations.append({
                    'category': 'Tempo',
                    'message': f'BPM ({bpm:.0f}) está acima do ideal. Considere reduzir para 110-130 BPM.',
                    'priority': 'medium'
                })
        
        # Danceability
        if 'danceability' in scores and scores['danceability'] < 0.6:
            recommendations.append({
                'category': 'Dançabilidade',
                'message': 'Baixa dançabilidade. Adicione elementos rítmicos mais marcados e regulares.',
                'priority': 'high'
            })
        
        # Energy
        if 'energy' in scores and scores['energy'] < 0.6:
            recommendations.append({
                'category': 'Energia',
                'message': 'Energia baixa. Considere aumentar a dinâmica e intensidade da produção.',
                'priority': 'medium'
            })
        
        # Duration
        if 'duration' in features:
            duration = features['duration']
            if duration > 240:
                recommendations.append({
                    'category': 'Duração',
                    'message': f'Música muito longa ({duration/60:.1f} min). Considere editar para 3-4 minutos.',
                    'priority': 'medium'
                })
            elif duration < 150:
                recommendations.append({
                    'category': 'Duração',
                    'message': f'Música muito curta ({duration/60:.1f} min). Considere expandir para 2.5-4 minutos.',
                    'priority': 'low'
                })
        
        # Se não há recomendações críticas
        if not recommendations:
            recommendations.append({
                'category': 'Geral',
                'message': 'Ótimas características! Continue refinando a produção e o mix.',
                'priority': 'low'
            })
        
        return recommendations
