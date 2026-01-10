import pandas as pd
import numpy as np
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Paths
INPUT_CSV = r"ml\datasets\github_hits\extracted\df_74_features.csv"
OUTPUT_CSV = r"ml\datasets\github_labeled.csv"
MODEL_PATH = r"ml\models\github_validation_model.pkl"

def integrate():
    print("=== Integrating GitHub Dataset ===")
    
    if not os.path.exists(INPUT_CSV):
        print(f"Error: Input file {INPUT_CSV} not found.")
        return

    # Load data
    df = pd.read_csv(INPUT_CSV)
    print(f"Loaded {len(df)} rows and {len(df.columns)} columns.")

    # Apply 441/441 split labeling (Hits/Non-Hits)
    # According to Bertoni et al. (SBBD 2021), dataset has 441 hits and 441 non-hits.
    df['is_hit'] = 0
    df.iloc[:441, df.columns.get_loc('is_hit')] = 1
    
    print(f"Labels assigned: {df['is_hit'].sum()} Hits, {len(df) - df['is_hit'].sum()} Non-Hits.")

    # Save labeled version
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"Saved labeled dataset to: {OUTPUT_CSV}")

    # Train a validation model to check if features are actually predictive
    print("\n=== Training Validation Model (74 Features) ===")
    
    # Drop index column and any non-numeric columns if they exist
    X = df.drop(['is_hit', 'Unnamed: 0'], axis=1)
    y = df['is_hit']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    
    print(f"Model Accuracy: {acc:.2%}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    # Save the model
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"Validation model saved to: {MODEL_PATH}")

    # Note about feature mapping
    print("\nNOTE: These 74 features are Essentia-extracted and anonymous.")
    print("Integration into active prediction requires mapping them to Librosa/Spotify features")
    print("or adding an Essentia extraction step to the backend.")

if __name__ == "__main__":
    integrate()
