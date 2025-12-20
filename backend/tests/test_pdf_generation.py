import sys
import os

# Add parent directory to path to import services
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.pdf_generator import generate_medical_report_pdf

def test_pdf_generation():
    """Test the PDF generation with sample data"""
    
    # Sample analysis data
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
            },
            "glucose": {
                "value": 105,
                "unit": "mg/dL",
                "status": "NORMAL",
                "reference_range": "70 - 100"
            }
        },
        "ckd_risk": {
            "level": "MODERATE",
            "score": 0.35
        },
        "medical_explanation": """Your lab results show some concerning values that require attention. 

Your creatinine level is elevated at 1.8 mg/dL, which is above the normal range. This indicates that your kidneys may not be filtering waste as efficiently as they should. Additionally, your eGFR (estimated Glomerular Filtration Rate) is 45 mL/min/1.73m², which is below the normal threshold and suggests reduced kidney function.

These findings, combined with your risk assessment, indicate a moderate risk for chronic kidney disease. While this is not an immediate emergency, it does require attention and lifestyle modifications.

Your BUN and glucose levels are within normal ranges, which is positive. However, the kidney function markers need to be monitored closely.""",
        "recommendations": [
            "Schedule an appointment with a nephrologist within 2-4 weeks for comprehensive evaluation",
            "Increase water intake to 8-10 glasses per day to support kidney function",
            "Reduce sodium intake to less than 2,300mg daily",
            "Monitor blood pressure regularly and maintain it below 130/80 mmHg",
            "Avoid NSAIDs (like ibuprofen) unless prescribed by your doctor",
            "Follow a kidney-friendly diet rich in fruits and vegetables",
            "Get regular exercise - aim for 30 minutes of moderate activity most days",
            "Schedule follow-up lab work in 3 months to monitor kidney function",
            "Limit protein intake as recommended by your healthcare provider",
            "Avoid smoking and limit alcohol consumption"
        ],
        "agent_decision": {
            "priority_level": "elevated",
            "urgency": "scheduled",
            "should_recommend_specialist": True,
            "focus_areas": ["creatinine", "egfr"],
            "key_concerns": ["Elevated risk of chronic kidney disease"]
        }
    }
    
    sample_patient = {
        "name": "John Doe",
        "age": 45,
        "id": "TEST-12345"
    }
    
    print("Generating PDF report...")
    
    try:
        # Generate PDF
        pdf_buffer = generate_medical_report_pdf(sample_data, sample_patient)
        
        # Save to file
        output_path = os.path.join(os.path.dirname(__file__), "test_medical_report.pdf")
        with open(output_path, 'wb') as f:
            f.write(pdf_buffer.getvalue())
        
        print(f"✓ PDF generated successfully!")
        print(f"✓ Saved to: {output_path}")
        print(f"✓ File size: {len(pdf_buffer.getvalue())} bytes")
        
        return True
        
    except Exception as e:
        print(f"✗ Error generating PDF: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_pdf_generation()
    sys.exit(0 if success else 1)
