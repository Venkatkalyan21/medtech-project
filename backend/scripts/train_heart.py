import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
import joblib
import os
import sys

# Define base paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(os.path.dirname(BASE_DIR), "heart1", "cardio.csv")
MODELS_DIR = os.path.join(BASE_DIR, "models")

# Create models directory if not exists
os.makedirs(MODELS_DIR, exist_ok=True)

def train_heart_model():
    print(f"Loading data from {DATA_PATH}...")
    try:
        df = pd.read_csv(DATA_PATH, sep=";") # Note: potential separator issue, checking first line if possible or assuming ; based on common cardio datasets
        # If read fails with default sep, try comma
        if df.shape[1] == 1:
            df = pd.read_csv(DATA_PATH, sep=",")
    except Exception as e:
        print(f"Error loading csv: {e}")
        # Try finding the file recursively if path is wrong
        return

    print(f"Data shape: {df.shape}")
    
    features = [
        "age", # in days usually
        "gender",
        "height",
        "weight", 
        "ap_hi",
        "ap_lo",
        "cholesterol",
        "gluc",
        "smoke",
        "alco",
        "active"
    ]
    
    # Check if columns exist, if not map them
    # The notebook usually used: age_years, bmi, etc. Let's look at the notebook logic content again
    # Notebook used: age_years, bmi, ap_hi, ap_lo, cholesterol, gluc, smoke, alco, active
    # We need to transform raw data to match feature engineering
    
    # Calculate age in years if 'age' is in days
    if 'age' in df.columns and 'age_years' not in df.columns:
        df['age_years'] = (df['age'] / 365.25).astype(int)
        
    # Calculate BMI
    if 'weight' in df.columns and 'height' in df.columns:
        df['bmi'] = df['weight'] / ((df['height'] / 100) ** 2)
        
    final_features = [
        "age_years",
        "bmi",
        "ap_hi",
        "ap_lo",
        "cholesterol",
        "gluc",
        "smoke",
        "alco",
        "active"
    ]
    
    X = df[final_features]
    
    # Scale data
    print("Scaling data...")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Train Isolation Forest
    print("Training Isolation Forest...")
    model = IsolationForest(
        n_estimators=300,
        contamination=0.05,   # top 5% anomalies
        random_state=42
    )
    model.fit(X_scaled)
    
    # Save assets
    print("Saving models...")
    joblib.dump(model, os.path.join(MODELS_DIR, "heart_model.pkl"))
    joblib.dump(scaler, os.path.join(MODELS_DIR, "heart_scaler.pkl"))
    
    print("✅ Heart anomaly model trained and saved.")

if __name__ == "__main__":
    train_heart_model()
