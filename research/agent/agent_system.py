"""
Intelligent Agent for Medical Lab Report Analysis
This agent decides the explanation flow and generates medical insights using Google Gemini
"""

import google.generativeai as genai
from typing import Dict, List, Any
from enum import Enum


class LabValueStatus(str, Enum):
    """Lab value status"""
    LOW = "LOW"
    NORMAL = "NORMAL"
    HIGH = "HIGH"


class CKDRiskLevel(str, Enum):
    """CKD risk levels"""
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    VERY_HIGH = "VERY_HIGH"


class MedicalAgent:
    """
    Intelligent agent that analyzes lab results and generates medical explanations
    """
    
    def __init__(self, api_key: str):
        """
        Initialize the agent with Google Gemini API
        
        Args:
            api_key: Google Gemini API key
        """
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def analyze_and_explain(
        self,
        lab_results: Dict[str, Dict],
        ckd_risk_level: str,
        ckd_risk_score: float
    ) -> Dict[str, Any]:
        """
        Complete agent workflow: analyze results and generate explanation
        
        Args:
            lab_results: Dictionary of lab values with their classifications
                Example: {
                    "creatinine": {
                        "value": 1.8,
                        "unit": "mg/dL",
                        "status": "HIGH",
                        "reference_range": "0.7 - 1.3"
                    }
                }
            ckd_risk_level: CKD risk level (LOW, MODERATE, HIGH, VERY_HIGH)
            ckd_risk_score: Risk score between 0.0 and 1.0
            
        Returns:
            Dictionary containing:
                - agent_decision: Decision details
                - medical_explanation: AI-generated explanation
                - recommendations: List of recommendations
        """
        # Step 1: Agent Decision - Analyze the situation
        agent_decision = self._make_decision(lab_results, ckd_risk_level, ckd_risk_score)
        
        # Step 2: Generate medical explanation using LLM
        medical_explanation = self._generate_explanation(
            lab_results, 
            ckd_risk_level, 
            ckd_risk_score, 
            agent_decision
        )
        
        # Step 3: Generate recommendations
        recommendations = self._generate_recommendations(
            lab_results, 
            ckd_risk_level, 
            agent_decision
        )
        
        return {
            "agent_decision": agent_decision,
            "medical_explanation": medical_explanation,
            "recommendations": recommendations
        }
    
    def _make_decision(
        self,
        lab_results: Dict[str, Dict],
        ckd_risk_level: str,
        ckd_risk_score: float
    ) -> Dict[str, Any]:
        """
        Agent decision-making: Determine how to handle the analysis
        """
        # Determine priority level
        priority_map = {
            "LOW": "routine",
            "MODERATE": "elevated",
            "HIGH": "high",
            "VERY_HIGH": "critical"
        }
        priority = priority_map.get(ckd_risk_level, "routine")
        
        # Identify focus areas (abnormal values)
        focus_areas = [
            lab_name for lab_name, result in lab_results.items()
            if result.get("status") in ["LOW", "HIGH"]
        ]
        
        # Determine explanation depth
        if ckd_risk_level in ["HIGH", "VERY_HIGH"]:
            depth = "comprehensive"
        elif ckd_risk_level == "MODERATE":
            depth = "detailed"
        else:
            depth = "standard"
        
        # Should recommend specialist?
        abnormal_count = len(focus_areas)
        should_see_specialist = (
            ckd_risk_level in ["HIGH", "VERY_HIGH"] or 
            abnormal_count >= 3
        )
        
        # Assess urgency
        urgency_map = {
            "VERY_HIGH": "immediate",
            "HIGH": "soon",
            "MODERATE": "scheduled",
            "LOW": "routine"
        }
        urgency = urgency_map.get(ckd_risk_level, "routine")
        
        # Identify key concerns
        concerns = []
        for lab_name, result in lab_results.items():
            value = result.get("value")
            status = result.get("status")
            
            if lab_name == "egfr" and value and value < 30:
                concerns.append("Severely reduced kidney function")
            elif lab_name == "creatinine" and value and value > 2.0:
                concerns.append("Significantly elevated creatinine")
            elif lab_name == "bun" and value and value > 40:
                concerns.append("High blood urea nitrogen")
            elif lab_name == "albumin" and value and value < 3.0:
                concerns.append("Low albumin levels")
        
        if ckd_risk_level in ["HIGH", "VERY_HIGH"]:
            concerns.append("Elevated risk of chronic kidney disease")
        
        if not concerns:
            concerns = ["No major concerns identified"]
        
        # Determine tone
        tone_map = {
            "VERY_HIGH": "serious_but_supportive",
            "HIGH": "concerned_but_reassuring",
            "MODERATE": "informative_and_cautious",
            "LOW": "reassuring_and_educational"
        }
        tone = tone_map.get(ckd_risk_level, "reassuring_and_educational")
        
        return {
            "priority_level": priority,
            "focus_areas": focus_areas,
            "explanation_depth": depth,
            "should_recommend_specialist": should_see_specialist,
            "urgency": urgency,
            "key_concerns": concerns,
            "explanation_tone": tone
        }
    
    def _generate_explanation(
        self,
        lab_results: Dict[str, Dict],
        ckd_risk_level: str,
        ckd_risk_score: float,
        agent_decision: Dict[str, Any]
    ) -> str:
        """
        Generate medical explanation using Google Gemini LLM
        """
        # Build prompt
        lab_summary = []
        for lab_name, result in lab_results.items():
            lab_summary.append(
                f"- {lab_name.upper()}: {result.get('value')} {result.get('unit')} "
                f"(Status: {result.get('status')}, Reference: {result.get('reference_range')})"
            )
        
        lab_summary_text = "\n".join(lab_summary)
        
        prompt = f"""You are a medical AI assistant helping to explain lab test results to patients. 
Your role is to provide clear, accurate, and compassionate explanations.

**Lab Test Results:**
{lab_summary_text}

**CKD Risk Assessment:**
- Risk Level: {ckd_risk_level}
- Risk Score: {ckd_risk_score:.2%}

**Analysis Context:**
- Priority: {agent_decision.get('priority_level', 'routine')}
- Focus Areas: {', '.join(agent_decision.get('focus_areas', []))}
- Key Concerns: {', '.join(agent_decision.get('key_concerns', []))}
- Urgency: {agent_decision.get('urgency', 'routine')}

**Instructions:**
1. Provide a clear, patient-friendly explanation of the lab results
2. Explain what each abnormal value means in simple terms
3. Discuss the CKD risk level and what it indicates
4. Use a {agent_decision.get('explanation_tone', 'reassuring')} tone
5. Provide {agent_decision.get('explanation_depth', 'standard')} level of detail
6. Avoid medical jargon where possible, or explain it when necessary
7. Be empathetic and supportive

Please generate a comprehensive medical explanation based on these results."""

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating explanation: {str(e)}"
    
    def _generate_recommendations(
        self,
        lab_results: Dict[str, Dict],
        ckd_risk_level: str,
        agent_decision: Dict[str, Any]
    ) -> List[str]:
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
    # Initialize agent with API key
    API_KEY = "AIzaSyBICK4IOn5gJXn0l9n61OuHu3Ayc4ZLBKU"
    agent = MedicalAgent(api_key=API_KEY)
    
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
