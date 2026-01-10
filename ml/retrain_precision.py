"""
Retreinamento para Máxima Precisão
Nova MPB e R&B Pop com datasets otimizados
"""
import sys
from pathlib import Path
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report, precision_recall_fscore_support
import joblib
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

def train_precision_model(genre, dataset_path):
    """Treina modelo otimizado para máxima precisão"""
    print(f"\n{'='*70}")
    print(f"TREINANDO PARA MAXIMA PRECISAO: {genre.upper().replace('_', ' ')}")
    print(f"{'='*70}\n")
    
    df = pd.read_csv(dataset_path)
    print(f"Dataset: {len(df)} musicas")
    print(f"Hits: {df['is_hit'].sum()} ({df['is_hit'].mean():.1%})")
    print(f"Non-hits: {len(df) - df['is_hit'].sum()} ({1-df['is_hit'].mean():.1%})")
    
    # Features
    ml_features = ['bpm', 'energy', 'danceability', 'loudness', 'valence',
                   'acousticness', 'instrumentalness', 'liveness', 'speechiness']
    available_features = [f for f in ml_features if f in df.columns]
    
    X = df[available_features].fillna(df[available_features].mean())
    y = df['is_hit']
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"Train: {len(X_train)} | Test: {len(X_test)}")
    
    # Treina com hiperparâmetros otimizados para precisão
    print("\nTreinando Random Forest (otimizado para precisao)...")
    model = RandomForestClassifier(
        n_estimators=300,  # Mais árvores
        max_depth=15,      # Mais profundidade
        min_samples_split=3,  # Menos restritivo
        min_samples_leaf=1,   # Menos restritivo
        max_features='sqrt',  # Melhor generalização
        random_state=42,
        n_jobs=-1,
        class_weight='balanced'  # Balanceia classes
    )
    
    model.fit(X_train, y_train)
    
    # Avalia
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    # Precision, Recall, F1 por classe
    precision, recall, f1, support = precision_recall_fscore_support(y_test, y_pred, average=None)
    
    # Cross-validation
    cv_scores = cross_val_score(model, X, y, cv=5)
    cv_mean = cv_scores.mean()
    cv_std = cv_scores.std()
    
    print(f"\nRESULTADOS:")
    print(f"  Accuracy: {accuracy:.2%}")
    print(f"  CV Mean: {cv_mean:.2%}")
    print(f"  CV Std: {cv_std:.2%}")
    print(f"\nMETRICAS POR CLASSE:")
    print(f"  Non-Hit - Precision: {precision[0]:.2%} | Recall: {recall[0]:.2%} | F1: {f1[0]:.2%}")
    print(f"  Hit     - Precision: {precision[1]:.2%} | Recall: {recall[1]:.2%} | F1: {f1[1]:.2%}")
    
    # Classification report
    print(f"\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Non-Hit', 'Hit']))
    
    # Salva
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_filename = f"{genre}_RandomForest_precision_{timestamp}.pkl"
    model_path = Path(__file__).parent / 'models' / model_filename
    model_path.parent.mkdir(exist_ok=True)
    
    joblib.dump(model, model_path)
    print(f"\nModelo salvo: {model_filename}")
    
    return {
        'accuracy': accuracy,
        'cv_mean': cv_mean,
        'precision_hit': precision[1],
        'recall_hit': recall[1],
        'precision_nonhit': precision[0],
        'recall_nonhit': recall[0],
        'model_path': str(model_path)
    }

def main():
    """Treina modelos de precisão"""
    print("\n" + "="*70)
    print("RETREINAMENTO PARA MAXIMA PRECISAO")
    print("="*70)
    
    datasets_dir = Path(__file__).parent / 'datasets'
    
    models = {
        'nova_mpb': 'nova_mpb_precision.csv',
        'rnb_pop': 'rnb_pop_precision.csv'
    }
    
    results = {}
    
    for genre, filename in models.items():
        dataset_path = datasets_dir / filename
        
        if not dataset_path.exists():
            print(f"\nAVISO: Dataset nao encontrado: {filename}")
            continue
        
        try:
            result = train_precision_model(genre, str(dataset_path))
            results[genre] = result
        except Exception as e:
            print(f"\nERRO ao treinar {genre}: {e}")
            import traceback
            traceback.print_exc()
    
    # Relatório
    print("\n" + "="*70)
    print("RELATORIO FINAL - MODELOS DE PRECISAO")
    print("="*70 + "\n")
    
    for genre, result in results.items():
        print(f"{genre.upper().replace('_', ' ')}:")
        print(f"  Accuracy: {result['accuracy']:.2%}")
        print(f"  CV Mean: {result['cv_mean']:.2%}")
        print(f"  Precision (Hit): {result['precision_hit']:.2%}")
        print(f"  Recall (Hit): {result['recall_hit']:.2%}")
        print(f"  Precision (Non-Hit): {result['precision_nonhit']:.2%}")
        print(f"  Recall (Non-Hit): {result['recall_nonhit']:.2%}")
        print(f"  Modelo: {Path(result['model_path']).name}")
        print()
    
    print("="*70)
    print("MODELOS DE MAXIMA PRECISAO PRONTOS!")
    print("="*70)
    
    return results

if __name__ == "__main__":
    main()
