import argparse
import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import roc_curve, auc

try:
    import seaborn as sns
except Exception:
    sns = None
import joblib

EXPECTED_CATEGORICAL = {"rbc", "pc", "pcc", "ba", "htn", "dm", "cad", "appet", "pe", "ane"}

LEAKAGE_COLS = ["pcv", "hemo", "sc"]   # NEW LINE


def find_target_column(df: pd.DataFrame, explicit: str | None = None) -> str | None:
    if explicit and explicit in df.columns:
        return explicit
    for name in ("class", "classification", "CKD", "ckd", "Class", "target"):
        if name in df.columns:
            return name
    return None


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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="ckd_real_merged.csv")
    parser.add_argument("--target")
    parser.add_argument("--outfile", default="kidney_model.pkl")
    parser.add_argument("--n-estimators", type=int, default=250)
    parser.add_argument("--test-size", type=float, default=0.2)
    args = parser.parse_args()

    df = pd.read_csv(args.input)
    df = df.drop_duplicates()

    # =====================
    # REMOVE LEAK FEATURES
    # =====================
    df = df.drop(columns=[c for c in LEAKAGE_COLS if c in df.columns])
    print("Removed leakage columns:", [c for c in LEAKAGE_COLS if c in df.columns])

    target_col = find_target_column(df, explicit=args.target)
    if target_col is None:
        print("Target column not found")
        sys.exit(1)

    print("Using target:", target_col)

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
            n_estimators=args.n_estimators,
            class_weight="balanced",
            random_state=42))
    ])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=args.test_size, random_state=42, stratify=y
    )

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # ========== FEATURE IMPORTANCE VISUALIZATION ==========
    

    # get classifier model
    rf = model.named_steps["clf"]

    # get full feature names after encoding
    feature_names = model.named_steps["preprocess"].get_feature_names_out()

    importances = rf.feature_importances_

    # sort descending
    indices = np.argsort(importances)[::-1]
    sorted_names = feature_names[indices]
    sorted_imp = importances[indices]

    print("\n====== FEATURE IMPORTANCE (TOP 20) ======")
    for n, i in zip(sorted_names[:20], sorted_imp[:20]):
        print(f"{n}: {i:.4f}")

    # bar graph
    plt.figure(figsize=(10,6))
    sns.barplot(x=sorted_imp[:15], y=sorted_names[:15], palette="viridis")
    plt.title("Top Feature Importance For CKD Prediction")
    plt.xlabel("Importance Score")
    plt.ylabel("Feature Name")
    plt.show()
    # ====================================================
    
# prediction probability for class 1
    y_prob = model.predict_proba(X_test)[:,1]

    fpr, tpr, thresholds = roc_curve(y_test, y_prob)
    roc_auc = auc(fpr, tpr)

    print("\nROC–AUC SCORE:", roc_auc)

    plt.figure(figsize=(6,6))
    plt.plot(fpr, tpr, color='red', lw=2, label=f"AUC = {roc_auc:.3f}")
    plt.plot([0,1], [0,1], color='black', linestyle='--')
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curve – CKD Model")
    plt.legend(loc="lower right")
    plt.show()

    print("\nTrain Accuracy:", model.score(X_train, y_train))
    print("Test Accuracy:", accuracy_score(y_test, y_pred))

    print(classification_report(y_test, y_pred))

    cm = confusion_matrix(y_test, y_pred)
    print(cm)

    joblib.dump(model, args.outfile)
    print("Model saved →", args.outfile)


if __name__ == "__main__":
    main()
