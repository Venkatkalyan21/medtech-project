import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import os
import sys

# Define base paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Assuming ml folder is at the same level as backend
ML_DIR = os.path.join(os.path.dirname(BASE_DIR), "ml")
DATA_PATH = os.path.join(ML_DIR, "ckd_real_merged.csv")
MODELS_DIR = os.path.join(BASE_DIR, "models")

# Constants from original script
EXPECTED_CATEGORICAL = {"rbc", "pc", "pcc", "ba", "htn", "dm", "cad", "appet", "pe", "ane"}
LEAKAGE_COLS = ["pcv", "hemo", "sc"]

def normalize_target_series(s: pd.Series) -> pd.Series:
    s_str = s.astype(str).str.strip().str.lower()
    mapped = s_str.map({
        "ckd": 1, "notckd": 0, "yes": 1, "no": 0,
        "present": 1, "notpresent": 0, "true": 1, "false": 0,
        "1": 1, "0": 0
    })
    numeric = pd.to_numeric(s, errors="coerce")
    return mapped.fillna(numeric)

def clean_features(X: pd.DataFrame) -> pd.DataFrame:
    for col in X.columns:
        ser = X[col]
        if ser.dtype == object or pd.api.types.is_string_dtype(ser):
            s = ser.astype(str).str.replace("\t", " ", regex=False).str.strip()
            s = s.replace(r'(?i)^(?:\?|na|nan|none)$', pd.NA, regex=True)
            s = s.replace(r'^\s*$', pd.NA, regex=True)
            conv = pd.to_numeric(s, errors="coerce")
            if conv.notna().sum() > 0:
                X[col] = conv.where(conv.notna(), s)
            else:
                X[col] = s
        else:
            X[col] = ser

    for col in list(X.columns):
        if X[col].dtype == object:
            conv = pd.to_numeric(X[col], errors="coerce")
            if conv.notna().sum() > 0:
                X[col] = conv
    
    num_cols = X.select_dtypes(include=[np.number]).columns
    for col in list(num_cols):
        med = X[col].median(skipna=True)
        if pd.isna(med):
            X.drop(columns=[col], inplace=True)
        else:
            X[col] = X[col].fillna(med)

    cat_cols = [c for c in X.columns if c not in num_cols]
    for col in cat_cols:
        X[col] = X[col].fillna("missing")

    return X

def make_onehot(handle_unknown="ignore"):
    try:
        return OneHotEncoder(handle_unknown=handle_unknown, sparse_output=False)
    except:
        return OneHotEncoder(handle_unknown=handle_unknown, sparse=False)

def train_ckd_model():
    print(f"Loading data from {DATA_PATH}...")
    if not os.path.exists(DATA_PATH):
        # Fallback to check other potential files if main one missing
        print(f"Data file not found at {DATA_PATH}")
        return

    df = pd.read_csv(DATA_PATH)
    df = df.drop_duplicates()

    # REMOVE LEAK FEATURES
    df = df.drop(columns=[c for c in LEAKAGE_COLS if c in df.columns])
    
    # Find target
    target_col = "classification" # defaulting to most likely name
    if target_col not in df.columns:
        for name in ("class", "CKD", "ckd", "Class", "target"):
            if name in df.columns:
                target_col = name
                break
    
    print(f"Using target: {target_col}")
    
    y = normalize_target_series(df[target_col])
    mask = y.notna()

    X = df.drop(columns=[target_col])[mask].reset_index(drop=True)
    y = y[mask].astype(int).reset_index(drop=True)

    X = clean_features(X)

    categorical_features = [c for c in EXPECTED_CATEGORICAL if c in X.columns]

    if categorical_features:
        preprocess = ColumnTransformer(
            [("cat", make_onehot(), categorical_features)],
            remainder="passthrough"
        )
    else:
        preprocess = ColumnTransformer([], remainder="passthrough")

    model = Pipeline([
        ("preprocess", preprocess),
        ("clf", RandomForestClassifier(
            n_estimators=250,
            class_weight="balanced",
            random_state=42))
    ])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print("Training model...")
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    print("Test Accuracy:", accuracy_score(y_test, y_pred))

    # Save
    outfile = os.path.join(MODELS_DIR, "kidney_model.pkl")
    joblib.dump(model, outfile)
    print(f"✅ CKD model trained and saved to {outfile}")

if __name__ == "__main__":
    train_ckd_model()
