"""
Medical Agent System
Leverages Google Gemini LLM for intelligent analysis of lab results
"""
import os
from typing import Dict, List, Any
import google.generativeai as genai

class MedicalAgent:
    def __init__(self, api_key: str = None):
        """
        Initialize the Medical Agent
        
        Args:
            api_key: Google Gemini API key (if None, loads from GEMINI_API_KEY env var)
        """
        if api_key is None:
            api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-pro")
    
    def analyze_and_explain(self, lab_results: Dict, ckd_risk_level: str, ckd_risk_score: float) -> Dict:
        """
        Analyze lab results and provide medical explanation
        
        Args:
            lab_results: Dict of lab results with values, units, status, reference ranges
            ckd_risk_level: Risk level (LOW, MODERATE, HIGH)
            ckd_risk_score: Risk score (0.0 to 1.0)
            
        Returns:
            Dict with agent_decision, medical_explanation, and recommendations
        """
        # Step 1: Make intelligent decision
        agent_decision = self._make_decision(lab_results, ckd_risk_level, ckd_risk_score)
        
        # Step 2: Generate medical explanation using LLM
        medical_explanation = self._generate_explanation(lab_results, ckd_risk_level, agent_decision)
        
        # Step 3: Generate recommendations
        recommendations = self._generate_recommendations(lab_results, ckd_risk_level, agent_decision)
        
        return {
            "agent_decision": agent_decision,
            "medical_explanation": medical_explanation,
            "recommendations": recommendations
        }
    
    def _make_decision(self, lab_results: Dict, ckd_risk_level: str, ckd_risk_score: float) -> Dict[str, Any]:
        """
        Make intelligent decision based on lab results
        """
        decision = {
            "priority_level": "normal",
            "urgency": "routine",
            "focus_areas": [],
            "explanation_depth": "basic",
            "should_recommend_specialist": False,
            "explanation_tone": "neutral",
            "key_concerns": []
        }
        
        # Analyze abnormalities
        abnormal_tests = [name for name, result in lab_results.items() if result.get("status") == "HIGH" or result.get("status") == "LOW"]
        
        if abnormal_tests:
            decision["focus_areas"] = abnormal_tests
        
        # Risk-based adjustments
        if ckd_risk_level == "HIGH":
            decision["priority_level"] = "elevated"
            decision["urgency"] = "urgent"
            decision["explanation_depth"] = "detailed"
            decision["should_recommend_specialist"] = True
            decision["explanation_tone"] = "informative_and_cautious"
            decision["key_concerns"].append("Elevated risk of chronic kidney disease")
        elif ckd_risk_level == "MODERATE":
            decision["priority_level"] = "elevated"
            decision["urgency"] = "scheduled"
            decision["explanation_depth"] = "detailed"
            decision["should_recommend_specialist"] = True
            decision["explanation_tone"] = "informative_and_cautious"
            decision["key_concerns"].append("Moderate risk of chronic kidney disease")
        else:
            decision["priority_level"] = "normal"
            decision["urgency"] = "routine"
            decision["explanation_depth"] = "basic"
            decision["explanation_tone"] = "neutral"
        
        return decision
    
    def _generate_explanation(self, lab_results: Dict, ckd_risk_level: str, agent_decision: Dict) -> str:
        """
        Generate medical explanation using LLM
        """
        lab_brief = ", ".join([
            f"{name}: {result.get('value')} ({result.get('status')})"
            for name, result in lab_results.items()
        ])
        
        prompt = f"""Based on these lab results and CKD risk assessment, provide a brief medical explanation.

**Lab Results Summary:**
{lab_brief}

**CKD Risk Level:** {ckd_risk_level}
**Should See Specialist:** {agent_decision.get('should_recommend_specialist', False)}
**Urgency:** {agent_decision.get('urgency', 'routine')}

Provide a concise, professional medical explanation suitable for a healthcare provider dashboard."""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Unable to generate explanation: {str(e)}"
    
    def _generate_recommendations(self, lab_results: Dict, ckd_risk_level: str, agent_decision: Dict) -> List[str]:
        """
        Generate personalized recommendations using LLM
        """
        lab_brief = ", ".join([
            f"{name}: {result.get('value')} ({result.get('status')})"
            for name, result in lab_results.items()
        ])
        
        prompt = f"""Based on these lab results and CKD risk assessment, provide 5-7 specific, actionable recommendations for the patient.

**Lab Results Summary:**
{lab_brief}

**CKD Risk Level:** {ckd_risk_level}
**Should See Specialist:** {agent_decision.get('should_recommend_specialist', False)}
**Urgency:** {agent_decision.get('urgency', 'routine')}

Provide recommendations as a numbered list. Include:
1. Immediate actions if needed
2. Lifestyle modifications
3. Dietary suggestions
4. Follow-up testing recommendations
5. When to seek medical attention

Format: Return only the numbered list, one recommendation per line."""
        
        try:
            response = self.model.generate_content(prompt)
            # Parse the response into a list
            recommendations = [
                line.strip() 
                for line in response.text.split('\n') 
                if line.strip() and (line.strip()[0].isdigit() or line.strip().startswith('-'))
            ]
            return recommendations[:7]  # Limit to 7 recommendations
        except Exception as e:
            return [
                "1. Consult with your healthcare provider about these results",
                "2. Follow up with recommended tests",
                "3. Maintain a healthy diet and lifestyle"
            ]


# Example usage
if __name__ == "__main__":
    # Initialize agent with API key from environment variable
    # Set GEMINI_API_KEY environment variable before running
    agent = MedicalAgent()
    
    # Sample lab results (this would come from your friend's backend)
    sample_lab_results = {
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
            "value": 28,
            "unit": "mg/dL",
            "status": "HIGH",
            "reference_range": "7 - 20"
        }
    }
    
    # Run agent analysis
    result = agent.analyze_and_explain(
        lab_results=sample_lab_results,
        ckd_risk_level="MODERATE",
        ckd_risk_score=0.35
    )
    
    # Print results
    print("=" * 60)
    print("AGENT DECISION:")
    print("=" * 60)
    for key, value in result["agent_decision"].items():
        print(f"{key}: {value}")
    
    print("\n" + "=" * 60)
    print("MEDICAL EXPLANATION:")
    print("=" * 60)
    print(result["medical_explanation"])
    
    print("\n" + "=" * 60)
    print("RECOMMENDATIONS:")
    print("=" * 60)
    for rec in result["recommendations"]:
        print(rec)
