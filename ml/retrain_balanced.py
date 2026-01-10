"""
Retreinamento com Datasets Balanceados
Treina modelos com distribuição equilibrada de hits/non-hits
"""
import sys
from pathlib import Path
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report
import joblib
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

def train_balanced_model(genre, dataset_path):
    """Treina modelo com dataset balanceado"""
    print(f"\n{'='*70}")
    print(f"TREINANDO: {genre.upper().replace('_', ' ')}")
    print(f"{'='*70}\n")
    
    df = pd.read_csv(dataset_path)
    print(f"Dataset: {len(df)} musicas")
    print(f"Hit ratio: {df['is_hit'].mean():.1%}")
    print(f"Hits: {df['is_hit'].sum()} | Non-hits: {len(df) - df['is_hit'].sum()}")
    
    # Verifica se tem non-hits suficientes
    nonhits = len(df) - df['is_hit'].sum()
    if nonhits < 2:
        print(f"\nAVISO: Poucos non-hits ({nonhits})")
        print("Pulando treinamento...")
        return None, None, None
    
    # Features
    ml_features = ['bpm', 'energy', 'danceability', 'loudness', 'valence',
                   'acousticness', 'instrumentalness', 'liveness', 'speechiness']
    available_features = [f for f in ml_features if f in df.columns]
    
    X = df[available_features].fillna(df[available_features].mean())
    y = df['is_hit']
    
    # Split (sem stratify se tiver poucos non-hits)
    try:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
    except:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
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
    
    try:
        cv_scores = cross_val_score(model, X, y, cv=5)
        cv_mean = cv_scores.mean()
        cv_std = cv_scores.std()
    except:
        cv_mean = accuracy
        cv_std = 0
    
    print(f"\nRESULTADOS:")
    print(f"  Accuracy: {accuracy:.2%}")
    print(f"  CV Mean: {cv_mean:.2%}")
    print(f"  CV Std: {cv_std:.2%}")
    
    # Classification report
    print(f"\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Non-Hit', 'Hit']))
    
    # Salva
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_filename = f"{genre}_RandomForest_balanced_{timestamp}.pkl"
    model_path = Path(__file__).parent / 'models' / model_filename
    model_path.parent.mkdir(exist_ok=True)
    
    joblib.dump(model, model_path)
    print(f"\nModelo salvo: {model_filename}")
    
    return accuracy, cv_mean, str(model_path)

def main():
    """Treina todos os modelos com datasets balanceados"""
    print("\n" + "="*70)
    print("RETREINAMENTO COM DATASETS BALANCEADOS")
    print("="*70)
    
    datasets_dir = Path(__file__).parent / 'datasets'
    
    subcategories = {
        'nova_mpb': 'nova_mpb_balanced.csv',
        'rnb_trap': 'rnb_trap_balanced.csv',
        'rnb_pop': 'rnb_pop_balanced.csv'
        # mpb_rock tem 99% hits, nao treina
    }
    
    results = {}
    
    for genre, filename in subcategories.items():
        dataset_path = datasets_dir / filename
        
        if not dataset_path.exists():
            print(f"\nAVISO: Dataset nao encontrado: {filename}")
            continue
        
        try:
            accuracy, cv_mean, model_path = train_balanced_model(genre, str(dataset_path))
            if accuracy is not None:
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
    print("RELATORIO FINAL - MODELOS BALANCEADOS")
    print("="*70 + "\n")
    
    for genre, result in results.items():
        print(f"{genre.upper().replace('_', ' ')}:")
        print(f"  Test Accuracy: {result['accuracy']:.2%}")
        print(f"  CV Mean: {result['cv_mean']:.2%}")
        print(f"  Modelo: {Path(result['model_path']).name}")
        print()
    
    print("="*70)
    print("RETREINAMENTO BALANCEADO CONCLUIDO!")
    print("="*70)
    
    return results

if __name__ == "__main__":
    main()
