from fastapi import APIRouter, HTTPException
from ml.model_predict import predict_ckd

router = APIRouter()

@router.post("/predict_ckd")
def ckd_api(data: dict):
    try:
        result = predict_ckd(data)
        return {"CKD_prediction": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
