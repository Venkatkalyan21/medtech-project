import sys
import os

# Add backend to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.ml_service import ml_service

print("Models loaded:", ml_service.models.keys())

data = {"age": 40}
print("Prediction:", ml_service.predict_ckd(data))
