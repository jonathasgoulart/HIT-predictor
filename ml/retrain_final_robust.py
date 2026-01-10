"""
Retreinamento Final com Datasets Robustos
Treina modelos para subcategorias com 70-114 músicas cada
"""
import sys
from pathlib import Path
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score
import joblib
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

def train_final_model(genre, dataset_path):
    """Treina modelo final para subcategoria"""
    print(f"\n{'='*70}")
    print(f"TREINANDO: {genre.upper().replace('_', ' ')}")
    print(f"{'='*70}\n")
    
    df = pd.read_csv(dataset_path)
    print(f"Dataset: {len(df)} musicas")
    print(f"Hit ratio: {df['is_hit'].mean():.1%}")
    
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
    
    # Treina
    print("\nTreinando Random Forest...")
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=12,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    
    # Avalia
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    cv_scores = cross_val_score(model, X, y, cv=5)
    cv_mean = cv_scores.mean()
    
    print(f"\nRESULTADOS:")
    print(f"  Accuracy: {accuracy:.2%}")
    print(f"  CV Mean: {cv_mean:.2%}")
    print(f"  CV Std: {cv_scores.std():.2%}")
    
    # Salva
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_filename = f"{genre}_RandomForest_final_{timestamp}.pkl"
    model_path = Path(__file__).parent / 'models' / model_filename
    model_path.parent.mkdir(exist_ok=True)
    
    joblib.dump(model, model_path)
    print(f"\nModelo salvo: {model_filename}")
    
    return accuracy, cv_mean, str(model_path)

def main():
    """Treina todos os modelos finais"""
    print("\n" + "="*70)
    print("RETREINAMENTO FINAL - DATASETS ROBUSTOS")
    print("="*70)
    
    datasets_dir = Path(__file__).parent / 'datasets'
    
    subcategories = {
        'mpb_rock': 'mpb_rock_final.csv',
        'nova_mpb': 'nova_mpb_final.csv',
        'rnb_trap': 'rnb_trap_final.csv',
        'rnb_pop': 'rnb_pop_final.csv'
    }
    
    results = {}
    
    for genre, filename in subcategories.items():
        dataset_path = datasets_dir / filename
        
        if not dataset_path.exists():
            print(f"\nAVISO: Dataset nao encontrado: {filename}")
            continue
        
        try:
            accuracy, cv_mean, model_path = train_final_model(genre, str(dataset_path))
            results[genre] = {
                'accuracy': accuracy,
                'cv_mean': cv_mean,
                'model_path': model_path
            }
        except Exception as e:
            print(f"\nERRO ao treinar {genre}: {e}")
            import traceback
            traceback.print_exc()
    
    # Relatório
    print("\n" + "="*70)
    print("RELATORIO FINAL - MODELOS ROBUSTOS")
    print("="*70 + "\n")
    
    for genre, result in results.items():
        print(f"{genre.upper().replace('_', ' ')}:")
        print(f"  Test Accuracy: {result['accuracy']:.2%}")
        print(f"  CV Mean: {result['cv_mean']:.2%}")
        print(f"  Modelo: {Path(result['model_path']).name}")
        print()
    
    print("="*70)
    print("RETREINAMENTO FINAL CONCLUIDO!")
    print("="*70)
    
    return results

if __name__ == "__main__":
    main()
