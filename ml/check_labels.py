"""
Check for labels and binary columns in GitHub dataset.
Also check for any hidden metadata.
"""
import pandas as pd
import numpy as np

df = pd.read_csv('datasets/github_hits/extracted/df_74_features.csv')

print("=== Column Statistics ===")
# Look for binary columns (only 0 and 1)
binary_cols = []
for col in df.columns:
    unique_vals = df[col].dropna().unique()
    if len(unique_vals) == 2 and set(unique_vals).issubset({0, 1, 0.0, 1.0}):
        binary_cols.append(col)

print(f"Binary columns found: {binary_cols}")
if binary_cols:
    for col in binary_cols:
        print(f"Distribution for {col}:")
        print(df[col].value_counts())

# Check the distribution of the first/last few rows to see if it's hit/non-hit split
# Assuming 441 hits followed by 441 non-hits (or vice versa)
print("\n=== Split Analysis (Top vs Bottom) ===")
first_half = df.iloc[:441, 1:] # Skip index column
second_half = df.iloc[441:, 1:]
print(f"First half mean (subset): {first_half.iloc[:, :5].mean().values}")
print(f"Second half mean (subset): {second_half.iloc[:, :5].mean().values}")

# Difference test
diff = (first_half.mean() - second_half.mean()).abs().sort_values(ascending=False)
print("\nTop 5 features with most difference between halves:")
print(diff.head(5))

# Check for labels in other rar files? 
# Only extracted df_74_features. Let's see if we can find a file with song names.
