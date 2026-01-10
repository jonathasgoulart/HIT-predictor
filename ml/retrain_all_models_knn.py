"""
Retreina TODOS os modelos usando datasets consolidados com KNN Imputation
Treina 7 gêneros com datasets expandidos
"""
import os
import sys
from pathlib import Path
from train_model import ModelTrainer

def train_consolidated_models():
    """Treina modelos usando datasets consolidados (KNN)"""
    
    print("="*70)
    print("RETREINAMENTO COM DATASETS EXPANDIDOS (KNN IMPUTATION)")
    print("="*70)
    print()
    
    # Datasets consolidados
    datasets_dir = Path(__file__).parent / 'datasets' / 'consolidated_knn'
    
    # Configuração de todos os gêneros
    datasets = [
        {
            'path': datasets_dir / 'mpb_consolidated.csv',
            'genre': 'MPB',
            'genre_id': 'mpb',
            'min_accuracy': 0.65,
            'n_estimators': 200,  # Mais árvores para dataset maior
            'max_depth': 15
        },
        {
            'path': datasets_dir / 'rnb_brasil_consolidated.csv',
            'genre': 'R&B Brasil',
            'genre_id': 'rnb_brasil',
            'min_accuracy': 0.65,
            'n_estimators': 200,
            'max_depth': 15
        },
        {
            'path': datasets_dir / 'sertanejo_consolidated.csv',
            'genre': 'Sertanejo',
            'genre_id': 'sertanejo',
            'min_accuracy': 0.60,
            'n_estimators': 150,  # Dataset médio
            'max_depth': 12
        },
        {
            'path': datasets_dir / 'pop_urban_brasil_consolidated.csv',
            'genre': 'Pop Urban Brasil',
            'genre_id': 'pop_urban_brasil',
            'min_accuracy': 0.60,
            'n_estimators': 150,
            'max_depth': 12
        },
        {
            'path': datasets_dir / 'forro_consolidated.csv',
            'genre': 'Forró',
            'genre_id': 'forro',
            'min_accuracy': 0.60,
            'n_estimators': 150,
            'max_depth': 12
        },
        {
            'path': datasets_dir / 'samba_consolidated.csv',
            'genre': 'Samba',
            'genre_id': 'samba',
            'min_accuracy': 0.60,
            'n_estimators': 150,
            'max_depth': 12
        },
        {
            'path': datasets_dir / 'pagode_consolidated.csv',
            'genre': 'Pagode',
            'genre_id': 'pagode',
            'min_accuracy': 0.60,
            'n_estimators': 150,
            'max_depth': 12
        }
    ]
    
    trained_models = []
    failed_models = []
    
    for idx, dataset_config in enumerate(datasets, 1):
        dataset_path = dataset_config['path']
        genre = dataset_config['genre']
        min_accuracy = dataset_config['min_accuracy']
        
        print(f"\n[{idx}/7] {'='*60}")
        print(f"TREINANDO: {genre}")
        print(f"{'='*60}\n")
        
        if not dataset_path.exists():
            print(f"ERRO: Dataset nao encontrado: {dataset_path}")
            failed_models.append(genre)
            continue
        
        try:
            # Inicializa trainer
            trainer = ModelTrainer(str(dataset_path))
            trainer.load_dataset()
            
            dataset_size = len(trainer.df)
            print(f"Dataset: {dataset_size} musicas")
            
            # Verifica distribuição de classes
            if 'is_hit' in trainer.df.columns:
                hits = trainer.df['is_hit'].sum()
                non_hits = dataset_size - hits
                print(f"  Hits: {hits} ({hits/dataset_size*100:.1f}%)")
                print(f"  Nao-hits: {non_hits} ({non_hits/dataset_size*100:.1f}%)")
            
            # Prepara dados
            test_size = 0.2 if dataset_size >= 100 else 0.3
            trainer.prepare_data(test_size=test_size)
            
            print(f"\nTreinando Random Forest...")
            print(f"  Estimators: {dataset_config['n_estimators']}")
            print(f"  Max depth: {dataset_config['max_depth']}")
            
            # Treina Random Forest
            trainer.train_random_forest(
                n_estimators=dataset_config['n_estimators'],
                max_depth=dataset_config['max_depth']
            )
            
            # Avalia
            metrics = trainer.evaluate()
            
            # Salva modelo
            model_path = trainer.save_model()
            
            # Resultados
            accuracy = metrics['accuracy']
            cv_mean = metrics['cv_mean']
            
            print(f"\n{'='*60}")
            print(f"RESULTADOS - {genre}")
            print(f"{'='*60}")
            print(f"  Accuracy:          {accuracy:.2%}")
            print(f"  CV Score (mean):   {cv_mean:.2%}")
            print(f"  Modelo salvo:      {Path(model_path).name}")
            
            # Verifica performance
            if accuracy >= min_accuracy:
                status = "OK"
                print(f"  Status:            {status} (>= {min_accuracy:.0%})")
            else:
                status = "ABAIXO DO ESPERADO"
                print(f"  Status:            {status} (< {min_accuracy:.0%})")
            
            trained_models.append({
                'genre': genre,
                'genre_id': dataset_config['genre_id'],
                'path': model_path,
                'accuracy': accuracy,
                'cv_score': cv_mean,
                'dataset_size': dataset_size,
                'status': status
            })
                    
        except Exception as e:
            print(f"\nERRO ao treinar modelo {genre}:")
            print(f"  {e}")
            import traceback
            traceback.print_exc()
            failed_models.append(genre)
    
    # Resumo final
    print("\n" + "="*70)
    print("RESUMO FINAL DO RETREINAMENTO")
    print("="*70)
    
    if trained_models:
        print(f"\nModelos treinados com sucesso: {len(trained_models)}/7\n")
        
        # Ordena por accuracy
        trained_models.sort(key=lambda x: x['accuracy'], reverse=True)
        
        print(f"{'Genero':<25} {'Dataset':<10} {'Accuracy':<12} {'CV Score':<12}")
        print("-"*70)
        for model in trained_models:
            print(f"{model['genre']:<25} {model['dataset_size']:<10} "
                  f"{model['accuracy']:>10.1%}  {model['cv_score']:>10.1%}")
    
    if failed_models:
        print(f"\n\nFalhas: {len(failed_models)}")
        for genre in failed_models:
            print(f"  X {genre}")
    
    print("\n" + "="*70)
    
    if len(trained_models) == 7:
        print("OK TODOS OS 7 MODELOS FORAM RETREINADOS COM SUCESSO!")
    elif trained_models:
        print(f"PARCIAL: {len(trained_models)}/7 modelos foram treinados")
    else:
        print("ERRO: Nenhum modelo foi treinado")
    
    print("="*70)
    print()
    
    # Salva relatório
    save_training_report(trained_models, failed_models)
    
    return trained_models, failed_models

def save_training_report(trained_models, failed_models):
    """Salva relatório do treinamento"""
    report_path = Path(__file__).parent / 'datasets' / 'consolidated_knn' / 'training_report.md'
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# Relatorio de Retreinamento de Modelos\n\n")
        f.write(f"Data: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("## Modelos Treinados\n\n")
        f.write("| Genero | Dataset | Accuracy | CV Score | Arquivo |\n")
        f.write("|--------|---------|----------|----------|---------|\\n")
        
        for model in sorted(trained_models, key=lambda x: x['accuracy'], reverse=True):
            filename = Path(model['path']).name
            f.write(f"| {model['genre']} | {model['dataset_size']} | "
                   f"{model['accuracy']:.1%} | {model['cv_score']:.1%} | {filename} |\n")
        
        if failed_models:
            f.write("\n## Falhas\n\n")
            for genre in failed_models:
                f.write(f"- {genre}\n")
        
        f.write("\n## Proximos Passos\n\n")
        f.write("1. Comparar com modelos anteriores\n")
        f.write("2. Gerar novo top 10 por genero\n")
        f.write("3. Atualizar modelos em producao\n")
    
    print(f"Relatorio salvo: {report_path}")

if __name__ == '__main__':
    trained, failed = train_consolidated_models()
    
    # Exit code
    if len(trained) == 7:
        sys.exit(0)  # Sucesso total
    elif trained:
        sys.exit(1)  # Sucesso parcial
    else:
        sys.exit(2)  # Falha total
