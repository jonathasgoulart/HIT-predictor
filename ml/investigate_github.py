"""
Investiga estrutura do dataset GitHub
"""
import pandas as pd

df = pd.read_csv('datasets/github_hits/extracted/df_74_features.csv')

print("=" * 60)
print("INVESTIGACAO DO DATASET")
print("=" * 60)

# Verifica primeira coluna (pode ser o índice ou classificação)
print("\nColuna 'Unnamed: 0':")
print(f"  Valores unicos: {df['Unnamed: 0'].nunique()}")
print(f"  Min: {df['Unnamed: 0'].min()}, Max: {df['Unnamed: 0'].max()}")
print(f"  Primeiros valores: {df['Unnamed: 0'].head(10).tolist()}")

# Verifica se é sequencial (índice) ou binário (classificação)
if df['Unnamed: 0'].nunique() == 2:
    print("\n  POSSIVEL CLASSIFICACAO HIT/NAO-HIT!")
    print(f"  Distribuicao:")
    print(df['Unnamed: 0'].value_counts())
elif df['Unnamed: 0'].nunique() == len(df):
    print("\n  Parece ser um indice sequencial")

# Verifica se há padrão nos dados
print("\n" + "=" * 60)
print("ESTATISTICAS DAS FEATURES")
print("=" * 60)

# Pega algumas colunas numéricas
numeric_cols = [col for col in df.columns if col != 'Unnamed: 0'][:5]
print(f"\nPrimeiras 5 features numericas:")
print(df[numeric_cols].describe())

# Verifica range dos valores
print(f"\nRange de valores:")
for col in numeric_cols:
    print(f"  {col}: [{df[col].min():.6f}, {df[col].max():.6f}]")

# Tenta encontrar documentação
print("\n" + "=" * 60)
print("PROCURANDO DOCUMENTACAO")
print("=" * 60)

# Verifica README
try:
    with open('datasets/github_hits/README.md', 'r', encoding='utf-8') as f:
        readme = f.read()
        print("\nREADME.md:")
        print(readme)
except Exception as e:
    print(f"Erro ao ler README: {e}")
