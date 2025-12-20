from fastapi import APIRouter, HTTPException
from database.mongo import reports_collection
from datetime import datetime
import uuid
from services.ocr_engine import extract_text_from_pdf
import os
from services.lab_extractor import extract_lab_values
from services.abnormality_engine import check_abnormalities
from services.health_score import generate_health_score
from services.agent_service import get_agent_analysis


router = APIRouter(prefix="/analyze", tags=["Analyze"])



@router.post("/{report_id}")
async def analyze_report(report_id: str):

    report = reports_collection.find_one({"report_id": report_id})
    
    
    file_path = os.path.join("uploads", report["file_name"])

    try:
        extracted_text = extract_text_from_pdf(file_path)
    except Exception as e:
        reports_collection.update_one(
            {"report_id": report_id},
            { "$set": {
                "status": "ocr_failed",
                "error": str(e)
            }}
        )
        raise HTTPException(status_code=500, detail="OCR failed")

    lab_values = extract_lab_values(extracted_text)

    if not lab_values or len(lab_values) == 0:
        reports_collection.update_one(
            {"report_id": report_id},
            { "$set": {
                "status": "no_values_found",
                "extracted_raw_text": extracted_text
            }}
        )
        return {
            "status": "no_values_found",
            "message": "OCR succeeded but no lab values detected",
            "raw_text_preview": extracted_text[:400]
        }

    alerts = check_abnormalities(lab_values)
    score = generate_health_score(alerts)
    
    # Get AI-powered agent analysis
    agent_analysis = get_agent_analysis(lab_values, alerts)

    reports_collection.update_one(
        {"report_id": report_id},
        {
            "$set": {
                "status": "extracted",
                "extracted_raw_text": extracted_text,
                "lab_values": lab_values,
                "alerts": alerts,
                "health_score": score,
                "agent_analysis": agent_analysis
            }
        }
    )
    print("OCR TEXT PREVIEW →")
    print(extracted_text[:700])

    return {
        "status": "extracted",
        "report_id": report_id,
        "lab_values": lab_values,
        "alerts": alerts,
        "health_score": score,
        "agent_analysis": agent_analysis
    }
