from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd
from pathlib import Path
import io

from ml.predict import parse_text_to_features, predict_from_features
from routes.upload_route import router as upload_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501"],  # Streamlit host
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = joblib.load("kidney_model.pkl")
app.include_router(upload_router)
class Patient(BaseModel):
    age: float
    bp: float
    bgr: float
    bu: float
    pcv: float
    htn: float
    dm: float
    rbc: float
    hemo: float
    pot: float
    sg: float

@app.post("/predict")
def predict_ckd(data: Patient):
    df = pd.DataFrame([data.dict()])
    pred = model.predict(df)[0]
    return {"CKD_Predict": int(pred)}

@app.post("/upload_report")
async def upload_report(file: UploadFile = File(...)):
    content = await file.read()
    filename = file.filename or ""
    text = ""

    # Image -> OCR
    if file.content_type and file.content_type.startswith("image"):
        try:
            from PIL import Image
            import pytesseract
            img = Image.open(io.BytesIO(content))
            text = pytesseract.image_to_string(img)
        except Exception as e:
            text = ""
    # PDF -> text via pdfplumber
    elif filename.lower().endswith(".pdf"):
        try:
            import pdfplumber
            with pdfplumber.open(io.BytesIO(content)) as pdf:
                pages = [p.extract_text() or "" for p in pdf.pages]
                text = "\n".join(pages)
        except Exception:
            text = ""
    # fallback: try decode as text
    else:
        try:
            text = content.decode("utf-8")
        except Exception:
            text = content.decode("latin1", errors="ignore")

    features = parse_text_to_features(text)
    pred, proba = predict_from_features(features)
    return {"extracted_text": text[:4000], "features": features, "prediction": int(pred), "probability": float(proba)}
