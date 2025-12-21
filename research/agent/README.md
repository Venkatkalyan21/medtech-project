# Medical Lab Report Analysis - Agent System

## 🤖 What is This?

This is a standalone **intelligent agent** that analyzes medical lab results and generates AI-powered explanations using Google Gemini.

Your friend handles the backend (OCR, parsing, rule engine, ML model), and this agent takes the results and:
1. **Decides** how to explain the results (priority, urgency, tone)
2. **Generates** medical explanations using AI
3. **Creates** personalized recommendations

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd agent
pip install -r requirements.txt
```

### 2. Use the Agent

```python
from agent_system import MedicalAgent

# Initialize with your API key
agent = MedicalAgent(api_key="AIzaSyBICK4IOn5gJXn0l9n61OuHu3Ayc4ZLBKU")

# Your friend's backend provides this data
lab_results = {
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
    }
}

# Run the agent
result = agent.analyze_and_explain(
    lab_results=lab_results,
    ckd_risk_level="MODERATE",
    ckd_risk_score=0.35
)

# Get the results
print(result["agent_decision"])      # Agent's decision
print(result["medical_explanation"]) # AI explanation
print(result["recommendations"])     # Recommendations
```

## 📋 Input Format

Your friend's backend should provide:

```python
{
    "lab_results": {
        "lab_name": {
            "value": float,
            "unit": str,
            "status": "LOW" | "NORMAL" | "HIGH",
            "reference_range": str
        }
    },
    "ckd_risk_level": "LOW" | "MODERATE" | "HIGH" | "VERY_HIGH",
    "ckd_risk_score": float  # 0.0 to 1.0
}
```

## 📤 Output Format

The agent returns:

```python
{
    "agent_decision": {
        "priority_level": str,           # routine, elevated, high, critical
        "focus_areas": list,             # Abnormal lab values
        "explanation_depth": str,        # standard, detailed, comprehensive
        "should_recommend_specialist": bool,
        "urgency": str,                  # routine, scheduled, soon, immediate
        "key_concerns": list,            # Medical concerns
        "explanation_tone": str          # How to communicate
    },
    "medical_explanation": str,          # AI-generated explanation
    "recommendations": list              # List of recommendations
}
```

## 🧪 Test the Agent

Run the example:

```bash
python agent_system.py
```

This will show you how the agent works with sample data.

## 🔗 Integration with Backend

Your friend's backend should call the agent like this:

```python
# After getting lab results, rule engine output, and ML prediction
from agent_system import MedicalAgent

agent = MedicalAgent(api_key="YOUR_API_KEY")

# Get agent analysis
agent_result = agent.analyze_and_explain(
    lab_results=classified_lab_results,
    ckd_risk_level=ml_prediction_level,
    ckd_risk_score=ml_prediction_score
)

# Add to API response
response = {
    "lab_values": classified_lab_results,
    "ckd_risk": {
        "level": ml_prediction_level,
        "score": ml_prediction_score
    },
    "agent_decision": agent_result["agent_decision"],
    "medical_explanation": agent_result["medical_explanation"],
    "recommendations": agent_result["recommendations"]
}
```

## 🎯 What the Agent Does

### 1. Decision Making
- Analyzes risk level and lab results
- Determines priority and urgency
- Identifies focus areas
- Decides if specialist is needed

### 2. AI Explanation
- Uses Google Gemini to generate explanations
- Tailors tone based on severity
- Explains in patient-friendly language
- Provides context for abnormal values

### 3. Recommendations
- Generates personalized advice
- Suggests lifestyle changes
- Recommends follow-up actions
- Indicates when to seek help

## 🔑 API Key

Your API key is already configured in the code:
```
AIzaSyBICK4IOn5gJXn0l9n61OuHu3Ayc4ZLBKU
```

## 📝 Example Output

```
AGENT DECISION:
priority_level: elevated
focus_areas: ['creatinine', 'egfr']
explanation_depth: detailed
should_recommend_specialist: True
urgency: scheduled
key_concerns: ['Elevated risk of chronic kidney disease']
explanation_tone: informative_and_cautious

MEDICAL EXPLANATION:
Your lab results show some concerning values that require attention...
[AI-generated detailed explanation]

RECOMMENDATIONS:
1. Schedule an appointment with a nephrologist within 2-4 weeks
2. Increase water intake to 8-10 glasses per day
3. Reduce sodium intake to less than 2,300mg daily
...
```

## 🤝 Working with Your Friend

**Your friend provides:**
- PDF upload
- OCR text extraction
- Lab value parsing
- Rule engine (LOW/NORMAL/HIGH)
- ML model (CKD risk prediction)

**Your agent provides:**
- Intelligent decision-making
- AI-powered explanations
- Personalized recommendations

**Together:** Complete medical analysis pipeline!

## 📦 Files

- `agent_system.py` - Main agent code
- `requirements.txt` - Dependencies
- `README.md` - This file

---

**Your agent is ready to use!** 🎉
