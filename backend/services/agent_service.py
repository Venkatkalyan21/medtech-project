"""
Agent Service Wrapper
Integrates the Medical Agent with the backend
"""
import os
from services.agent_system import MedicalAgent

# Load API key from environment variable
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is not set")

agent = MedicalAgent(api_key=API_KEY)


def format_lab_results_for_agent(lab_values, alerts):
    """
    Convert backend lab values and alerts to agent format
    
    Args:
        lab_values: Dict of lab values from backend
        alerts: Dict of abnormality alerts from backend
        
    Returns:
        Formatted dict for agent
    """
    formatted_results = {}
    
    for test_name, value in lab_values.items():
        alert_info = alerts.get(test_name, {})
        status = alert_info.get("status", "UNKNOWN")
        
        # Get reference range (you can customize this based on your normal_ranges)
        from services.normal_ranges import normal_ranges
        ref_range = "N/A"
        if test_name in normal_ranges:
            low, high = normal_ranges[test_name]
            ref_range = f"{low} - {high}"
        
        formatted_results[test_name] = {
            "value": value,
            "unit": get_unit_for_test(test_name),
            "status": status,
            "reference_range": ref_range
        }
    
    return formatted_results


def get_unit_for_test(test_name):
    """Get the unit for a given test"""
    units = {
        "creatinine": "mg/dL",
        "egfr": "mL/min/1.73m²",
        "bun": "mg/dL",
        "glucose": "mg/dL",
        "hemoglobin": "g/dL",
        "albumin": "g/dL",
        "protein": "g/dL",
        "cholesterol": "mg/dL",
        "triglycerides": "mg/dL",
        "hdl": "mg/dL",
        "ldl": "mg/dL",
    }
    return units.get(test_name.lower(), "")


def calculate_ckd_risk(lab_values, alerts):
    """
    Calculate CKD risk level and score based on lab values
    
    Args:
        lab_values: Dict of lab values
        alerts: Dict of abnormality alerts
        
    Returns:
        Tuple of (risk_level, risk_score)
    """
    risk_score = 0.0
    
    # Check for kidney function indicators
    creatinine = lab_values.get("creatinine")
    egfr = lab_values.get("egfr") or lab_values.get("eGFR")
    bun = lab_values.get("bun") or lab_values.get("BUN")
    
    # eGFR-based risk
    if egfr is not None:
        if egfr < 15:
            risk_score += 0.4
        elif egfr < 30:
            risk_score += 0.35
        elif egfr < 60:
            risk_score += 0.25
        elif egfr < 90:
            risk_score += 0.1
    
    # Creatinine-based risk
    if creatinine is not None:
        if creatinine > 3.0:
            risk_score += 0.3
        elif creatinine > 2.0:
            risk_score += 0.2
        elif creatinine > 1.5:
            risk_score += 0.1
    
    # BUN-based risk
    if bun is not None:
        if bun > 40:
            risk_score += 0.2
        elif bun > 25:
            risk_score += 0.1
    
    # Determine risk level
    if risk_score >= 0.35:
        risk_level = "HIGH"
    elif risk_score >= 0.2:
        risk_level = "MODERATE"
    else:
        risk_level = "LOW"
    
    return risk_level, risk_score
