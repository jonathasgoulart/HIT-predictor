# import numpy as np
# import joblib
import os
from pathlib import Path

class HitPredictor:
    """Modelo de predição baseado em heurísticas de características de hits"""
    
    # Features usadas pelo modelo ML (9 features compatíveis com Spotify)
    ML_FEATURES = ['bpm', 'energy', 'danceability', 'valence',
                   'acousticness', 'instrumentalness', 'liveness',
                   'speechiness', 'loudness']
    
    # Cache global de modelos para evitar recarregamento pesado do disco (economia de RAM)
    _model_cache = {}
    
    def __init__(self, genre=None):
        """
        Inicializa preditor
        
        Args:
            genre: Gênero musical ('mpb', 'rnb_brasil', ou None para genérico)
        """
        # Alias para compatibilidade
        if genre == 'brazil':
            genre = 'pop_urban_brasil'
            
        self.genre = genre
        self.ml_model = None
        self.scaler = None
        self.model_type = 'heuristic' # default
        
        # Estratégia por gênero (ATUALIZADO com subcategorias - Jan 2026)
        # 'ml': usa modelo ML, 'heuristic': usa apenas heurística
        self.GENRE_STRATEGY = {
            # Subcategorias NOVAS (modelos especializados)
            'rnb_trap': 'ml',          # 78% accuracy (EXCELENTE)
            'rnb_pop': 'ml',           # 75% accuracy (BOM)
            'mpb_rock': 'ml',          # 65% accuracy (RAZOÁVEL)
            
            # Gêneros com auto-detecção de subcategoria
            'rnb_brasil': 'ml',        # Auto-detecta trap vs pop
            'mpb': 'ml',               # Usa MPB Rock por padrão
            
            # Outros gêneros (sem mudanças)
            'forro': 'heuristic',
            'samba': 'ml',             # 71.43% accuracy
            'pagode': 'ml',            # 62.50% accuracy
            'brazil': 'ml',
            'pop_urban_brasil': 'ml',  # 62.50% accuracy
            'sertanejo': 'ml'          # 70.83% accuracy
        }
        
        # Tenta carregar modelo ML se gênero especificado
        if genre:
            self._load_ml_model(genre)
        
        # Ranges ideais padrão (Genérico) - RIGOR MÁXIMO (Alinhado com Top 50% Hits)
        self.ideal_ranges = {
            'bpm': (118, 126),       # Range Pop extremamente competitivo
            'energy': (0.7, 0.85),   # Músicas muito cansativas ou muito calmas perdem pontos
            'loudness': (-7.5, -5.5), # Loudness comercial de masterização (dBFS A-weighted)
            'danceability': (0.75, 0.9), # Batida deve ser clara e constante
            'brightness': (2200, 2800),
            'dynamic_variation': (0.18, 0.28)
        }
        
        # Pesos para cada característica (total = 100)
        self.weights = {
            'bpm': 10,
            'energy': 20,
            'danceability': 40,      # Groove é o critério #1
            'loudness': 10,
            'brightness': 10,
            'dynamic_variation': 10
        }

        # Ajustes específicos por gênero (BASEADO EM CORRELAÇÕES REAIS!)
        if genre == 'mpb_rock':
            # MPB Rock: Requer mais energia e peso
            self.ideal_ranges.update({
                'bpm': (105, 145),
                'energy': (0.65, 0.90),        # Mais restrito para Rock
                'danceability': (0.4, 0.75),
                'acousticness': (0.05, 0.35),   # Menos acústico que Indie
                'loudness': (-8.5, -4.5),       # Mais barulhento
                'speechiness': (0.03, 0.12),
                'valence': (0.4, 0.85)
            })
            self.weights = {
                'energy': 35,
                'loudness': 25,
                'bpm': 15,
                'acousticness': 15,
                'danceability': 5,
                'valence': 5
            }
        
        elif genre == 'mpb_indie':
            # MPB Indie: Mais suave, acústico e "vibe"
            self.ideal_ranges.update({
                'bpm': (85, 125),
                'energy': (0.35, 0.65),
                'acousticness': (0.45, 0.90),
                'loudness': (-12.0, -7.0),
                'valence': (0.3, 0.7)
            })
            self.weights = {
                'acousticness': 40,
                'energy': 20,
                'valence': 20,
                'bpm': 10,
                'speechiness': 10
            }
        
        # Ajustes para Pop Urban Brasil (Funk, Pop, Trap)
        # Precisa aceitar desde baladas (90 bpm) até Funk 150 (130-150 bpm)
        elif genre == 'pop_urban_brasil' or genre == 'brazil':
            self.ideal_ranges.update({
                'bpm': (90, 150),
                'energy': (0.4, 0.95),
                'danceability': (0.5, 0.95),
                'loudness': (-12.0, -3.0) 
            })
            self.weights = {
                 'bpm': 15,
                 'energy': 20,
                 'danceability': 40, # Dançabilidade é rei no Brasil
                 'loudness': 15,
                 'brightness': 5,
                 'dynamic_variation': 5
            }

        elif genre == 'rnb_brasil':
            self.ideal_ranges.update({
                'bpm': (70, 105),
                'energy': (0.5, 0.75),
                'danceability': (0.6, 0.85),
                'loudness': (-10, -6)
            })
            self.weights = { # Foco em groove e energia moderada
                'bpm': 10,
                'energy': 20,
                'danceability': 40,
                'loudness': 10,
                'brightness': 10,
                'dynamic_variation': 10
            }
        elif genre == 'sertanejo':
            # Sertanejo: BPM NEGATIVO (-0.211), Energy (+0.178), Loudness (+0.167)
            # Valence (+0.133), Acousticness (-0.125 NEGATIVO)
            self.ideal_ranges.update({
                'bpm': (80, 150),  # AMPLO (baladas E animadas)
                'energy': (0.55, 0.85),
                'danceability': (0.55, 0.8),
                'loudness': (-8.0, -5.0),
                'valence': (0.4, 0.8),
                'acousticness': (0.1, 0.4)  # Hits têm MENOS acústico
            })
            self.weights = {
                'bpm': 0,  # ZERO (correlação negativa)
                'energy': 35,  # TOP feature
                'danceability': 10,
                'loudness': 30,  # Segunda mais importante
                'valence': 15,
                'acousticness': 10  # Penaliza se muito alto
            }
        elif genre == 'pagode':
            # Pagode: Acousticness é TOP (+0.286), Speechiness negativa
            self.ideal_ranges.update({
                'bpm': (90, 125),
                'energy': (0.6, 0.85),
                'danceability': (0.5, 0.87)  # Não é tão importante (corr +0.042)
            })
            self.weights = {
                'bpm': 10,
                'energy': 20,
                'danceability': 10,  # REDUZIDO (correlação fraca)
                'loudness': 15,
                'brightness': 35,  # Proxy para acousticness
                'dynamic_variation': 10
            }
        
        elif genre == 'samba':
            # Samba: ENERGY é rei (+0.537)! BPM também importante (+0.336)
            self.ideal_ranges.update({
                'bpm': (92, 121),  # Range real dos hits
                'energy': (0.48, 0.88),
                'danceability': (0.46, 0.88)  # Não importa (corr +0.045)
            })
            self.weights = {
                'bpm': 25,  # Segunda feature mais importante
                'energy': 45,  # TOP ABSOLUTA!
                'danceability': 5,  # Quase inútil
                'loudness': 10,
                'brightness': 10,
                'dynamic_variation': 5
            }

        elif genre == 'pop_urban_brasil':
            self.ideal_ranges.update({
                'bpm': (90, 150),
                'energy': (0.4, 0.95), 
                'danceability': (0.5, 0.95)
            })
            self.weights = { 
                'bpm': 15,
                'energy': 25,
                'danceability': 35,
                'loudness': 10,
                'brightness': 10,
                'dynamic_variation': 5
            }

        elif genre == 'forro':
            # Forró: Energy (+0.481), Loudness (+0.304), Valence (+0.260)
            self.ideal_ranges.update({
                'bpm': (143, 159),  # Range real dos hits
                'energy': (0.73, 0.87),
                'danceability': (0.53, 0.87)  # Correlação NEGATIVA (-0.157)!
            })
            self.weights = {
                'bpm': 20,  # Moderadamente importante (+0.232)
                'energy': 35,  # TOP feature
                'danceability': 5,  # REDUZIDO (correlação negativa!)
                'loudness': 25,  # Segunda feature mais importante
                'brightness': 10,
                'dynamic_variation': 5
            }
    
    def _load_ml_model(self, genre):
        """Carrega modelo ML treinado para o gênero especificado"""
        print(f"    [PREDICTOR] Tentando carregar modelo para: {genre}")
        try:
            # Caminho para diretório de modelos
            models_dir = Path(__file__).parent.parent / 'ml' / 'models'
            
            # Mapeamento para legacy ID 'brazil' -> 'pop_urban_brasil'
            target_genre = genre
            if genre == 'brazil':
                target_genre = 'pop_urban_brasil'
            
            # Prioridade de modelos (melhor para pior)
            # 1. Enhanced (com feature engineering) - 70%+
            # 2. Basic/GitHub (modelos simples) - 54-60%
            # 3. Qualquer outro modelo
            
            model_priorities = [
                f"{target_genre}_RandomForest_enhanced_*.pkl",  # Prioridade 1
                f"{target_genre}_RF_basic_*.pkl",               # Prioridade 2
                f"{target_genre}_RF_github_*.pkl",              # Prioridade 3
                f"{target_genre}_*.pkl"                         # Fallback
            ]
            
            latest_model = None
            for pattern in model_priorities:
                model_files = list(models_dir.glob(pattern))
                if model_files:
                    # Pega o mais recente
                    latest_model = sorted(model_files)[-1]
                    break
            
            if latest_model:
                model_path = str(latest_model)
                
                # Verifica se o modelo já está no cache
                if model_path in self._model_cache:
                    self.ml_model = self._model_cache[model_path]
                    print(f"    [OK] Modelo ML recuperado do cache: {latest_model.name}")
                else:
                    import joblib
                    self.ml_model = joblib.load(latest_model)
                    self._model_cache[model_path] = self.ml_model
                    print(f"    [OK] Modelo ML carregado: {latest_model.name}")
                
                self.model_type = 'ml'
            else:
                print(f"    [INFO] Nenhum modelo ML encontrado para '{genre}', usando heuristicas")
                
        except Exception as e:
            print(f"    [ERRO] Ao carregar modelo ML: {e}")
            print("    [INFO] Usando heuristicas como fallback")
    
    def _prepare_ml_features(self, features):
        """Prepara features no formato esperado pelo modelo ML"""
        import numpy as np
        ml_input = []
        for feature_name in self.ML_FEATURES:
            # Mapeia nomes de features
            if feature_name == 'duration_ms':
                # No backend vem em segundos, ML quer em milissegundos
                # Se não existir, assume 3:30 (210000ms)
                value = features.get('duration', 210.0) * 1000
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
        """
        Normaliza score baseado em range ideal com penalidade LINEAR moderada.
        Garante distribuição equilibrada (30-100%) para todos os gêneros.
        """
        # Garante que value é real (não complexo)
        try:
            value = abs(value) if isinstance(value, complex) else float(value)
            ideal_min = float(ideal_min)
            ideal_max = float(ideal_max)
        except (TypeError, ValueError):
            return 0.5  # Fallback seguro
        
        if value < ideal_min:
            distance = ideal_min - value
            # Penalidade LINEAR moderada
            rel_distance = distance / (ideal_min if ideal_min != 0 else 1)
            penalty = min(rel_distance * 0.7, 0.7)  # Máximo 70% de penalidade
            return max(0.3, 1.0 - penalty)  # Mínimo 30%
            
        elif value > ideal_max:
            distance = value - ideal_max
            rel_distance = distance / (ideal_max if ideal_max != 0 else 1)
            penalty = min(rel_distance * 0.7, 0.7)
            return max(0.3, 1.0 - penalty)
            
        else:
            # Valor dentro do range ideal dá 100%
            return 1.0
    
    def calculate_bpm_score(self, bpm):
        """Calcula score do BPM (Sem bônus para evitar inflação)"""
        return self.normalize_score(bpm, *self.ideal_ranges['bpm'])
    
    def calculate_energy_score(self, energy):
        """Calcula score de energia"""
        return self.normalize_score(energy, *self.ideal_ranges['energy'])
    
    def calculate_danceability_score(self, danceability):
        """Calcula score de dançabilidade (Sem bônus para evitar inflação)"""
        return self.normalize_score(danceability, *self.ideal_ranges['danceability'])
    
    def calculate_loudness_score(self, loudness):
        """Calcula score de loudness"""
        return self.normalize_score(loudness, *self.ideal_ranges['loudness'])
    
    def calculate_brightness_score(self, brightness):
        """Calcula score de brightness (claridade espectral)"""
        return self.normalize_score(brightness, *self.ideal_ranges['brightness'])
    
    def calculate_variation_score(self, variation):
        """Calcula score de variação dinâmica"""
        return self.normalize_score(variation, *self.ideal_ranges['dynamic_variation'])
    
    # Spotify-specific features
    def calculate_acousticness_score(self, acousticness):
        """Calcula score de acousticness (Spotify feature)"""
        if 'acousticness' in self.ideal_ranges:
            return self.normalize_score(acousticness, *self.ideal_ranges['acousticness'])
        return 0.5

    def calculate_speechiness_score(self, speechiness):
        """Calcula score de speechiness (Spotify feature)"""
        if 'speechiness' in self.ideal_ranges:
            return self.normalize_score(speechiness, *self.ideal_ranges['speechiness'])
        return 0.5

    def calculate_valence_score(self, valence):
        """Calcula score de valence (Spotify feature)"""
        if 'valence' in self.ideal_ranges:
            return self.normalize_score(valence, *self.ideal_ranges['valence'])
        return 0.5

    def calculate_instrumentalness_score(self, instrumentalness):
        """Calcula score de instrumentalness (Spotify feature)"""
        if 'instrumentalness' in self.ideal_ranges:
            return self.normalize_score(instrumentalness, *self.ideal_ranges['instrumentalness'])
        return 0.5

    def calculate_liveness_score(self, liveness):
        """Calcula score de liveness (Spotify feature)"""
        if 'liveness' in self.ideal_ranges:
            return self.normalize_score(liveness, *self.ideal_ranges['liveness'])
        return 0.5
    
    def _calculate_heuristic_score(self, features):
        """Calcula score heurístico baseado nas features e pesos"""
        scores = {}
        
        # 1. Calcula scores individuais (0-1) usando as faixas ideais
        # Se a feature não existir, assume neutro (0.5) ou penaliza? vamos assumir neutro.
        
        # BPM
        scores['bpm'] = self.calculate_bpm_score(features.get('bpm', 120))
        
        # Energy
        scores['energy'] = self.calculate_energy_score(features.get('energy', 0.5))
        
        # Danceability
        scores['danceability'] = self.calculate_danceability_score(features.get('danceability', 0.5))
        
        # Loudness
        scores['loudness'] = self.calculate_loudness_score(features.get('loudness', -10))
        
        # Brightness (Spectral Centroid)
        brightness = features.get('brightness', 3000)
        # Normalizamos brightness para usar na score (ideal_ranges esperam valores absolutos ou relativos?)
        # Na init, não temos ranges para brightness explicitos no código que vi, 
        # mas vamos assumir que existe ou usar lógica simples se faltar.
        # Vou usar lógica genérica se não tiver no dicionário.
        if 'brightness' in self.ideal_ranges:
             scores['brightness'] = self.normalize_score(brightness, *self.ideal_ranges['brightness'])
        else:
             scores['brightness'] = 1.0 # Ignora se não configurado
             
        # Dynamic Variation
        if 'dynamic_variation' in self.ideal_ranges:
            scores['dynamic_variation'] = self.calculate_variation_score(features.get('dynamic_variation', 0.5))
        else:
            scores['dynamic_variation'] = 1.0

        # 2. Aplica pesos
        total_score = 0
        total_weight = 0
        
        for feature, weight in self.weights.items():
            if feature in scores:
                total_score += scores[feature] * weight
                total_weight += weight
        
        # 3. Normaliza para 0-100
        if total_weight > 0:
            final_heuristic_score = int((total_score / total_weight) * 100)
        else:
            final_heuristic_score = 50 # Fallback
            
        return final_heuristic_score, scores

    
    def detect_subcategory(self, features, genre):
        """
        Detecta subcategoria baseado em features de áudio
        Usado para R&B Brasil (trap vs pop) e MPB (rock vs indie)
        """
        if genre == 'rnb_brasil':
            bpm = features.get('bpm', 100)
            speechiness = features.get('speechiness', 0.1)
            valence = features.get('valence', 0.5)
            
            # R&B Trap: BPM baixo + alta speechiness
            if bpm < 95 and speechiness > 0.15:
                return 'rnb_trap'
            # R&B Pop: BPM médio + baixa speechiness + valence positiva
            elif bpm >= 95 and speechiness < 0.15 and valence > 0.4:
                return 'rnb_pop'
            # Default: R&B Trap (maioria)
            return 'rnb_trap'
        
        elif genre == 'mpb':
            # Detecção inteligente de subcategoria MPB
            energy = features.get('energy', 0.5)
            acousticness = features.get('acousticness', 0.5)
            loudness = features.get('loudness', -8)
            bpm = features.get('bpm', 110)
            valence = features.get('valence', 0.5)
            speechiness = features.get('speechiness', 0.1)
            
            # Score para cada subcategoria
            rock_score = 0
            indie_score = 0
            classic_score = 0
            
            # MPB ROCK: Alta energia, loudness alto, BPM médio-alto
            if energy > 0.6:
                rock_score += 30
            if loudness > -7:
                rock_score += 25
            if bpm > 110:
                rock_score += 20
            if acousticness < 0.4:
                rock_score += 15
            if speechiness < 0.15:
                rock_score += 10
            
            # MPB INDIE: Acústico, valence médio, BPM médio
            if acousticness > 0.5:
                indie_score += 30
            if 0.4 <= valence <= 0.7:
                indie_score += 25
            if 95 <= bpm <= 120:
                indie_score += 20
            if 0.4 <= energy <= 0.65:
                indie_score += 15
            if 0.05 <= speechiness <= 0.2:
                indie_score += 10
            
            # MPB CLÁSSICO: Muito acústico, BPM baixo, suave
            if acousticness > 0.7:
                classic_score += 35
            if bpm < 100:
                classic_score += 25
            if loudness < -9:
                classic_score += 20
            if energy < 0.5:
                classic_score += 15
            if speechiness < 0.1:
                classic_score += 5
            
            # Decide baseado no maior score
            scores = {
                'mpb_rock': rock_score,
                'mpb_indie': indie_score,
                'mpb_classic': classic_score
            }
            
            detected = max(scores, key=scores.get)
            max_score = scores[detected]
            
            # Log da decisão
            print(f"[MPB DETECTION] Scores: Rock={rock_score}, Indie={indie_score}, Classic={classic_score}")
            print(f"[MPB DETECTION] Detectado: {detected} (score={max_score})")
            
            # Se score muito baixo, usa Rock como default
            if max_score < 30:
                print("[MPB DETECTION] Score baixo, usando MPB Rock como default")
                return 'mpb_rock'
            
            # Por enquanto, só temos modelos para Rock e Indie
            # Se detectar Classic, usa Rock como fallback
            if detected == 'mpb_classic':
                print("[MPB DETECTION] Classic detectado, mas usando Rock como fallback (modelo não disponível)")
                return 'mpb_rock'
            
            return detected
        
        return genre
    
    def _predict_mpb_indie_ensemble(self, features):
        """
        Ensemble específico para MPB Indie
        Combina ML (40%) + Heurística (60%)
        """
        # Score Heurístico
        heuristic_score = 50
        
        # Acousticness
        acousticness = features.get('acousticness', 0.5)
        if acousticness > 0.6:
            heuristic_score += 15
        elif acousticness < 0.3:
            heuristic_score -= 10
        
        # Energy vs Valence
        energy = features.get('energy', 0.5)
        valence = features.get('valence', 0.5)
        if energy < 0.6 and valence > 0.5:
            heuristic_score += 15
        elif energy > 0.7 and valence < 0.4:
            heuristic_score -= 10
        
        # BPM
        bpm = features.get('bpm', 110)
        if 95 <= bpm <= 125:
            heuristic_score += 10
        elif bpm < 80 or bpm > 140:
            heuristic_score -= 10
        
        # Speechiness
        speechiness = features.get('speechiness', 0.1)
        if 0.05 <= speechiness <= 0.2:
            heuristic_score += 10
        elif speechiness > 0.3:
            heuristic_score -= 15
        
        # Danceability
        danceability = features.get('danceability', 0.5)
        if 0.4 <= danceability <= 0.7:
            heuristic_score += 10
        elif danceability > 0.8:
            heuristic_score -= 10
        
        # Normaliza
        heuristic_score = min(max(heuristic_score, 0), 100)
        
        # Tenta usar ML
        ml_score = None
        if hasattr(self, 'model') and self.model:
            try:
                ml_result = self._predict_with_ml(features)
                if ml_result:
                    ml_score = ml_result['ml_score']
            except:
                pass
        
        # Combina
        if ml_score is not None:
            final_score = (0.4 * ml_score) + (0.6 * heuristic_score)
            method = 'ensemble'
        else:
            final_score = heuristic_score
            method = 'heuristic_only'
        
        return {
            'final_score': int(round(final_score)),
            'heuristic_score': int(round(heuristic_score)),
            'ml_score': int(round(ml_score)) if ml_score else None,
            'method': method
        }
    
    def predict(self, features, genre='generic'):
        """
        Gera score de hit baseado em features de áudio.
        Retorna dicionário com score final e breakdown.
        """
        # Auto-detecta subcategoria se aplicável
        original_genre = self.genre
        if self.genre in ['rnb_brasil', 'mpb']:
            detected_genre = self.detect_subcategory(features, self.genre)
            if detected_genre != self.genre:
                print(f"[AUTO-DETECT] {self.genre} -> {detected_genre}")
                # Recarrega modelo com subcategoria detectada
                self._load_ml_model(detected_genre)
        
        # Determina estratégia (ML ou heurística)
        print(f"\n[PREDICTOR] Analisando para genero: {self.genre}")
        print(f"Input Features: BPM={features.get('bpm')}, Energy={features.get('energy'):.2f}, Dance={features.get('danceability'):.2f}")
        
        # ESPECIAL: MPB Indie usa ensemble
        if self.genre == 'mpb_indie':
            print("[PREDICTOR] Usando ENSEMBLE para MPB Indie")
            ensemble_result = self._predict_mpb_indie_ensemble(features)
            
            return {
                'hit_score': ensemble_result['final_score'],
                'prediction_method': ensemble_result['method'],
                'breakdown': {
                    'heuristic_score': ensemble_result['heuristic_score'],
                    'ml_score': ensemble_result['ml_score'],
                    'ensemble_weights': '40% ML + 60% Heurística' if ensemble_result['ml_score'] else '100% Heurística',
                    'genre': self.genre
                }
            }
        
        # 1. Calcula score heurístico (Base)
        heuristic_score, scores = self._calculate_heuristic_score(features)
        
        # Tenta usar modelo ML APENAS se a estratégia do gênero for 'ml'
        ml_result = None
        genre_strategy = self.GENRE_STRATEGY.get(self.genre, 'ml')  # Default para ML
        
        if self.ml_model and genre_strategy == 'ml':
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
        
        if 'brightness' in features:
            scores['brightness'] = self.calculate_brightness_score(features['brightness'])
        
        if 'dynamic_variation' in features:
            scores['dynamic_variation'] = self.calculate_variation_score(features['dynamic_variation'])
        
        # Calcula score ponderado total (heurístico)
        total_score = 0
        for feature, score in scores.items():
            if feature in self.weights:
                total_score += score * self.weights[feature]
        
        heuristic_score = min(int(round(total_score)), 100)
        
        # Decide qual score usar
        if ml_result:
            # Usa score ML, mas mantém heurístico para comparação
            ml_raw_score = ml_result['ml_score']
            final_score = ml_raw_score
            prediction_method = 'ml'
            
            # --- HYBRID SAFETY BOOST ---
            # Se o modelo ML estiver pessimista (< 75) mas a heuristica disser que é um golaço (> 70),
            # nós confiamos parcialmente na heurística.
            if ml_raw_score < 75 and heuristic_score > 70:
                boost = (heuristic_score - ml_raw_score) * 0.5
                final_score += boost
                final_score = min(int(round(final_score)), 100)
            
            # Adiciona breakdown para debug
            breakdown = ["Score Baseado em ML"]
            if final_score != ml_raw_score:
                breakdown.append(f"[Hybrid Boost] ML({ml_raw_score}) -> Final({final_score})")
            
            if ml_raw_score < 60 and heuristic_score > 80:
                breakdown.append(f"[Discrepancia] ML({ml_raw_score}) vs Heuristica({heuristic_score})")
        else:
            final_score = heuristic_score
            prediction_method = 'heuristic'
            
            # Gera breakdown das penalidades heurísticas
            breakdown = []
            for feature, score in scores.items():
                if score < 0.7: # Se score da feature for baixo
                    range_min, range_max = self.ideal_ranges.get(feature, (0,0))
                    val = features.get(feature, 0)
                    breakdown.append(f"Penalidade em {feature}: {val:.2f} (Ideal: {range_min}-{range_max})")
        
        # BOOST UNIVERSAL REMOVIDO PARA MELHOR CALIBRAÇÃO
        # final_score = min(final_score + 15, 100)
        
        result = {
            'hit_score': final_score,
            'prediction_method': prediction_method,
            'individual_scores': {k: round(v * 100, 1) for k, v in scores.items()},
            'recommendations': self.generate_recommendations(features, scores),
            'breakdown': breakdown
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
        
        # Se não há recomendações críticas
        if not recommendations:
            recommendations.append({
                'category': 'Geral',
                'message': 'Ótimas características! Continue refinando a produção e o mix.',
                'priority': 'low'
            })
        
        return recommendations
