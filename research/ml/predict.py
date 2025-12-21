import re
import joblib
from pathlib import Path
import pandas as pd
import numpy as np

BASE = Path(__file__).resolve().parent
MODEL = joblib.load(BASE / "kidney_model.pkl")
TRAIN = pd.read_csv(BASE / "ckd_real_merged.csv")
FEATURE_COLS = [c for c in TRAIN.columns if c != "class"]
MEDIANS = TRAIN[TRAIN.select_dtypes(include="number").columns].median()

# simple regex patterns for common labs; extend as needed
_PATTERNS = {
    "age": r"age[:\s]+(\d{1,3})",
    "bp": r"(?:bp|blood pressure)[:\s]+(\d{2,3})",
    "bgr": r"(?:bgr|glucose|blood glucose)[:\s]+(\d{2,4})",
    "bu": r"(?:bu|blood urea)[:\s]+(\d{1,3})",
    "pcv": r"(?:pcv|packed cell volume)[:\s]+(\d{1,3})",
    "hemo": r"(?:hemo|min h?emoglobin)[:\s]+(\d{1,3}\.?\d*)",
    "pot": r"(?:potassium|k\+|pot)[:\s]+(\d{1,3}\.?\d*)",
    "sg": r"(?:specific gravity|sg)[:\s]+(\d\.\d{2,3})",
}

BOOL_KEYWORDS = {
    "htn": ["hypertension", "htn"],
    "dm": ["diabetes", "dm"],
    "cad": ["cad", "coronary"],
    "pe": ["edema", "proteinuria", "pe"],
}

def _find_number(text: str, pattern: str):
    m = re.search(pattern, text, re.I)
    return float(m.group(1)) if m else None

def parse_text_to_features(text: str) -> dict:
    text = (text or "").lower()
    out = {}
    # numeric patterns
    for k, pat in _PATTERNS.items():
        val = _find_number(text, pat)
        if val is not None:
            out[k] = float(val)
    # boolean flags from keywords
    for k, words in BOOL_KEYWORDS.items():
        out[k] = 1 if any(w in text for w in words) else 0
    # simple mapping for presence/absence fields (rbc/pc etc.)
    # if keywords appear, set as 'abnormal' or 'normal'
    if "red blood cell" in text or "rbc" in text:
        out.setdefault("rbc", "abnormal" if "abnormal" in text else "normal")
    if "pus cell" in text or "pc" in text:
        out.setdefault("pc", "abnormal" if "abnormal" in text else "normal")
    return out

def _prepare_row(features: dict) -> pd.DataFrame:
    row = {c: None for c in FEATURE_COLS}
    # copy parsed features
    for k, v in features.items():
        if k in row:
            row[k] = v
    # fill numerics with medians
    for c in TRAIN.select_dtypes(include="number").columns:
        if c in row and (row[c] is None or (isinstance(row[c], float) and pd.isna(row[c]))):
            row[c] = MEDIANS.get(c, 0)
    # categorical fill
    for c in FEATURE_COLS:
        if row[c] is None:
            row[c] = "missing" if c not in TRAIN.select_dtypes(include="number").columns else MEDIANS.get(c, 0)
    return pd.DataFrame([row], columns=FEATURE_COLS)

def predict_from_features(features: dict):
    X = _prepare_row(features)
    pred = MODEL.predict(X)[0]
    proba = None
    try:
        proba = MODEL.predict_proba(X)[0][1]
    except Exception:
        proba = float(pred)
    return int(pred), float(proba)