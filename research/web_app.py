import streamlit as st
import pandas as pd
import joblib
from pathlib import Path
import requests

BASE = Path(__file__).resolve().parents[1]
MODEL_PATH = BASE / "ml" / "kidney_model.pkl"

model = joblib.load(MODEL_PATH)

TRAIN_CSV = BASE / "ml" / "ckd_real_merged.csv"
train_df = pd.read_csv(TRAIN_CSV)

FEATURE_COLS = [c for c in train_df.columns if c != "class"]
numeric_cols = train_df.select_dtypes(include="number").columns
MEDIANS = train_df[numeric_cols].median()
st.title("CKD Prediction - Full Report Form (22 Inputs)")

inputs = {}

for col in FEATURE_COLS:

    if train_df[col].dtype == "float64" or train_df[col].dtype == "int64":
        inputs[col] = st.number_input(
            f"{col}", value=float(MEDIANS[col])
        )

    else:
        unique_vals = train_df[col].dropna().unique().tolist()
        inputs[col] = st.selectbox(
            f"{col}", unique_vals
        )

if st.button("Predict"):

    df = pd.DataFrame([inputs], columns=FEATURE_COLS)

    pred = model.predict(df)[0]

    if int(pred) == 1:
        st.error("⚠ CKD Detected!")
    else:
        st.success("✔ CKD Not Detected!")

st.header("Or upload a lab report (PDF / image / txt)")
uploaded = st.file_uploader("Upload lab report", type=["pdf", "txt", "png", "jpg", "jpeg"])
if uploaded:
    # send file to backend
    resp = requests.post(
        "http://127.0.0.1:8000/upload_report",
        files={"file": (uploaded.name, uploaded.getvalue(), uploaded.type or "application/octet-stream")},
        timeout=30
    )
    if resp.ok:
        data = resp.json()
        st.subheader("Extracted text (preview)")
        st.text_area("Extracted", data.get("extracted_text", ""), height=300)
        st.subheader("Parsed features")
        st.json(data.get("features", {}))
        st.subheader("Prediction")
        pred = data.get("prediction")
        prob = data.get("probability")
        if pred == 1:
            st.error(f"CKD Detected — probability {prob:.2f}")
        else:
            st.success(f"CKD Not Detected — probability {prob:.2f}")
    else:
        st.error(f"Upload failed: {resp.status_code} {resp.text}")
