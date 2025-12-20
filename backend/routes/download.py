from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from services.pdf_generator import generate_medical_report_pdf
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime

router = APIRouter(prefix="/download", tags=["download"])

class PatientInfo(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    id: Optional[str] = None

class DownloadRequest(BaseModel):
    analysis_data: Dict[str, Any]
    patient_info: Optional[PatientInfo] = None

@router.post("/pdf")
async def download_pdf_report(request: DownloadRequest):
    """
    Generate and download a PDF report of the medical analysis
    
    Args:
        request: Contains analysis_data and optional patient_info
        
    Returns:
        PDF file as a streaming response
    """
    try:
        # Convert patient_info to dict if provided
        patient_dict = None
        if request.patient_info:
            patient_dict = request.patient_info.model_dump(exclude_none=True)
        
        # Generate PDF
        pdf_buffer = generate_medical_report_pdf(
            analysis_data=request.analysis_data,
            patient_info=patient_dict
        )
        
        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"medical_report_{timestamp}.pdf"
        
        # Return as streaming response
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating PDF report: {str(e)}"
        )

@router.get("/test-pdf")
async def test_pdf_generation():
    """
    Test endpoint to generate a sample PDF report
    """
    # Sample data for testing
    sample_data = {
        "lab_values": {
            "creatinine": {
                "value": 1.8,
                "unit": "mg/dL",
                "status": "HIGH",
                "reference_range": "0.7 - 1.3"
            },
            "egfr": {
                "value": 45,
                "unit": "mL/min/1.73m²",
                "status": "LOW",
                "reference_range": "> 90"
            },
            "bun": {
                "value": 25,
                "unit": "mg/dL",
                "status": "NORMAL",
                "reference_range": "7 - 20"
            }
        },
        "ckd_risk": {
            "level": "MODERATE",
            "score": 0.35
        },
        "medical_explanation": """Your lab results show some concerning values that require attention. 
        
Your creatinine level is elevated at 1.8 mg/dL, which is above the normal range. This indicates that your kidneys may not be filtering waste as efficiently as they should. Additionally, your eGFR (estimated Glomerular Filtration Rate) is 45 mL/min/1.73m², which is below the normal threshold and suggests reduced kidney function.

These findings, combined with your risk assessment, indicate a moderate risk for chronic kidney disease. While this is not an immediate emergency, it does require attention and lifestyle modifications.""",
        "recommendations": [
            "Schedule an appointment with a nephrologist within 2-4 weeks for comprehensive evaluation",
            "Increase water intake to 8-10 glasses per day to support kidney function",
            "Reduce sodium intake to less than 2,300mg daily",
            "Monitor blood pressure regularly and maintain it below 130/80 mmHg",
            "Avoid NSAIDs (like ibuprofen) unless prescribed by your doctor",
            "Follow a kidney-friendly diet rich in fruits and vegetables",
            "Get regular exercise - aim for 30 minutes of moderate activity most days",
            "Schedule follow-up lab work in 3 months to monitor kidney function"
        ],
        "agent_decision": {
            "priority_level": "elevated",
            "urgency": "scheduled",
            "should_recommend_specialist": True
        }
    }
    
    sample_patient = {
        "name": "Test Patient",
        "age": 45,
        "id": "TEST-001"
    }
    
    try:
        pdf_buffer = generate_medical_report_pdf(sample_data, sample_patient)
        
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition": "attachment; filename=test_medical_report.pdf"
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating test PDF: {str(e)}"
        )
