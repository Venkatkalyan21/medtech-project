from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.platypus import Image as RLImage
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from io import BytesIO
from datetime import datetime
import os

class MedicalReportPDFGenerator:
    """
    Generates professional PDF reports for medical lab analysis results
    """
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles for the report"""
        
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a237e'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#283593'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        # Subsection style
        self.styles.add(ParagraphStyle(
            name='SubSection',
            parent=self.styles['Heading3'],
            fontSize=12,
            textColor=colors.HexColor('#3949ab'),
            spaceAfter=8,
            spaceBefore=8,
            fontName='Helvetica-Bold'
        ))
        
        # Body text style
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['BodyText'],
            fontSize=11,
            textColor=colors.HexColor('#212121'),
            spaceAfter=6,
            alignment=TA_JUSTIFY,
            leading=14
        ))
        
        # Risk level style
        self.styles.add(ParagraphStyle(
            name='RiskLevel',
            parent=self.styles['Normal'],
            fontSize=14,
            spaceAfter=10,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
    
    def generate_report(self, analysis_data: dict, patient_info: dict = None) -> BytesIO:
        """
        Generate a complete medical analysis PDF report
        
        Args:
            analysis_data: Dictionary containing analysis results
            patient_info: Optional patient information
            
        Returns:
            BytesIO object containing the PDF
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Container for the 'Flowable' objects
        elements = []
        
        # Add header
        elements.extend(self._create_header(patient_info))
        elements.append(Spacer(1, 0.3*inch))
        
        # Add lab results section
        if 'lab_values' in analysis_data or 'lab_results' in analysis_data:
            elements.extend(self._create_lab_results_section(
                analysis_data.get('lab_values') or analysis_data.get('lab_results', {})
            ))
            elements.append(Spacer(1, 0.3*inch))
        
        # Add risk assessment section
        if 'ckd_risk' in analysis_data:
            elements.extend(self._create_risk_assessment_section(analysis_data['ckd_risk']))
            elements.append(Spacer(1, 0.3*inch))
        
        # Add AI explanation section
        if 'medical_explanation' in analysis_data:
            elements.extend(self._create_explanation_section(analysis_data['medical_explanation']))
            elements.append(Spacer(1, 0.3*inch))
        
        # Add recommendations section
        if 'recommendations' in analysis_data:
            elements.extend(self._create_recommendations_section(analysis_data['recommendations']))
            elements.append(Spacer(1, 0.3*inch))
        
        # Add agent decision section (optional)
        if 'agent_decision' in analysis_data:
            elements.extend(self._create_agent_decision_section(analysis_data['agent_decision']))
            elements.append(Spacer(1, 0.3*inch))
        
        # Add footer/disclaimer
        elements.extend(self._create_footer())
        
        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        return buffer
    
    def _create_header(self, patient_info: dict = None) -> list:
        """Create the report header"""
        elements = []
        
        # Title
        title = Paragraph("Medical Lab Analysis Report", self.styles['CustomTitle'])
        elements.append(title)
        elements.append(Spacer(1, 0.2*inch))
        
        # Report date
        report_date = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        date_text = Paragraph(f"<b>Report Generated:</b> {report_date}", self.styles['CustomBody'])
        elements.append(date_text)
        
        # Patient info if provided
        if patient_info:
            elements.append(Spacer(1, 0.1*inch))
            if 'name' in patient_info:
                elements.append(Paragraph(f"<b>Patient:</b> {patient_info['name']}", self.styles['CustomBody']))
            if 'age' in patient_info:
                elements.append(Paragraph(f"<b>Age:</b> {patient_info['age']}", self.styles['CustomBody']))
            if 'id' in patient_info:
                elements.append(Paragraph(f"<b>Patient ID:</b> {patient_info['id']}", self.styles['CustomBody']))
        
        # Divider line
        elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def _create_lab_results_section(self, lab_results: dict) -> list:
        """Create the lab results table section"""
        elements = []
        
        # Section header
        header = Paragraph("Laboratory Test Results", self.styles['SectionHeader'])
        elements.append(header)
        elements.append(Spacer(1, 0.1*inch))
        
        # Create table data
        table_data = [['Test Name', 'Value', 'Unit', 'Status', 'Reference Range']]
        
        for test_name, test_data in lab_results.items():
            if isinstance(test_data, dict):
                value = test_data.get('value', 'N/A')
                unit = test_data.get('unit', '')
                status = test_data.get('status', 'UNKNOWN')
                ref_range = test_data.get('reference_range', 'N/A')
                
                # Format test name (capitalize and replace underscores)
                formatted_name = test_name.replace('_', ' ').title()
                
                table_data.append([
                    formatted_name,
                    str(value),
                    unit,
                    status,
                    ref_range
                ])
        
        # Create table
        table = Table(table_data, colWidths=[2*inch, 1*inch, 1*inch, 1*inch, 1.5*inch])
        
        # Style the table
        table_style = TableStyle([
            # Header row
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3949ab')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            
            # Body
            ('ALIGN', (1, 1), (2, -1), 'CENTER'),
            ('ALIGN', (3, 1), (3, -1), 'CENTER'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
        ])
        
        # Color code status column
        for i, row in enumerate(table_data[1:], start=1):
            status = row[3]
            if status == 'HIGH':
                table_style.add('TEXTCOLOR', (3, i), (3, i), colors.HexColor('#d32f2f'))
                table_style.add('FONTNAME', (3, i), (3, i), 'Helvetica-Bold')
            elif status == 'LOW':
                table_style.add('TEXTCOLOR', (3, i), (3, i), colors.HexColor('#f57c00'))
                table_style.add('FONTNAME', (3, i), (3, i), 'Helvetica-Bold')
            elif status == 'NORMAL':
                table_style.add('TEXTCOLOR', (3, i), (3, i), colors.HexColor('#388e3c'))
        
        table.setStyle(table_style)
        elements.append(table)
        
        return elements
    
    def _create_risk_assessment_section(self, ckd_risk: dict) -> list:
        """Create the CKD risk assessment section"""
        elements = []
        
        # Section header
        header = Paragraph("Chronic Kidney Disease Risk Assessment", self.styles['SectionHeader'])
        elements.append(header)
        elements.append(Spacer(1, 0.1*inch))
        
        # Risk level
        risk_level = ckd_risk.get('level', 'UNKNOWN')
        risk_score = ckd_risk.get('score', 0.0)
        
        # Color code based on risk level
        risk_colors = {
            'LOW': '#388e3c',
            'MODERATE': '#f57c00',
            'HIGH': '#d32f2f',
            'VERY_HIGH': '#b71c1c'
        }
        risk_color = risk_colors.get(risk_level, '#757575')
        
        risk_text = f'<font color="{risk_color}"><b>Risk Level: {risk_level}</b></font>'
        risk_para = Paragraph(risk_text, self.styles['RiskLevel'])
        elements.append(risk_para)
        
        # Risk score
        score_text = f"Risk Score: <b>{risk_score:.2%}</b>"
        score_para = Paragraph(score_text, self.styles['CustomBody'])
        elements.append(score_para)
        
        # Risk interpretation
        elements.append(Spacer(1, 0.1*inch))
        interpretation = self._get_risk_interpretation(risk_level)
        interp_para = Paragraph(interpretation, self.styles['CustomBody'])
        elements.append(interp_para)
        
        return elements
    
    def _get_risk_interpretation(self, risk_level: str) -> str:
        """Get interpretation text for risk level"""
        interpretations = {
            'LOW': 'Your test results indicate a low risk of chronic kidney disease. Continue maintaining a healthy lifestyle.',
            'MODERATE': 'Your test results show moderate risk factors for chronic kidney disease. Consider lifestyle modifications and regular monitoring.',
            'HIGH': 'Your test results indicate elevated risk for chronic kidney disease. Consultation with a healthcare provider is recommended.',
            'VERY_HIGH': 'Your test results show significant risk factors for chronic kidney disease. Immediate consultation with a nephrologist is strongly recommended.'
        }
        return interpretations.get(risk_level, 'Risk assessment is pending.')
    
    def _create_explanation_section(self, explanation: str) -> list:
        """Create the AI-generated medical explanation section"""
        elements = []
        
        # Section header
        header = Paragraph("Medical Analysis & Explanation", self.styles['SectionHeader'])
        elements.append(header)
        elements.append(Spacer(1, 0.1*inch))
        
        # Explanation text
        # Split into paragraphs if there are line breaks
        paragraphs = explanation.split('\n\n')
        for para_text in paragraphs:
            if para_text.strip():
                para = Paragraph(para_text.strip(), self.styles['CustomBody'])
                elements.append(para)
                elements.append(Spacer(1, 0.05*inch))
        
        return elements
    
    def _create_recommendations_section(self, recommendations: list) -> list:
        """Create the recommendations section"""
        elements = []
        
        # Section header
        header = Paragraph("Personalized Recommendations", self.styles['SectionHeader'])
        elements.append(header)
        elements.append(Spacer(1, 0.1*inch))
        
        # Recommendations list
        for i, rec in enumerate(recommendations, 1):
            rec_text = f"<b>{i}.</b> {rec}"
            rec_para = Paragraph(rec_text, self.styles['CustomBody'])
            elements.append(rec_para)
            elements.append(Spacer(1, 0.05*inch))
        
        return elements
    
    def _create_agent_decision_section(self, agent_decision: dict) -> list:
        """Create the agent decision section (optional detailed info)"""
        elements = []
        
        # Section header
        header = Paragraph("Analysis Details", self.styles['SubSection'])
        elements.append(header)
        elements.append(Spacer(1, 0.1*inch))
        
        # Priority and urgency
        priority = agent_decision.get('priority_level', 'N/A')
        urgency = agent_decision.get('urgency', 'N/A')
        
        details_text = f"<b>Priority:</b> {priority.title()} | <b>Urgency:</b> {urgency.title()}"
        details_para = Paragraph(details_text, self.styles['CustomBody'])
        elements.append(details_para)
        
        # Specialist recommendation
        if agent_decision.get('should_recommend_specialist'):
            specialist_text = "<b>Specialist Consultation:</b> Recommended"
            specialist_para = Paragraph(specialist_text, self.styles['CustomBody'])
            elements.append(specialist_para)
        
        return elements
    
    def _create_footer(self) -> list:
        """Create the report footer with disclaimer"""
        elements = []
        
        # Divider
        elements.append(Spacer(1, 0.3*inch))
        
        # Disclaimer
        disclaimer_style = ParagraphStyle(
            name='Disclaimer',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#757575'),
            alignment=TA_JUSTIFY,
            leading=11
        )
        
        disclaimer_text = """
        <b>IMPORTANT DISCLAIMER:</b> This report is generated by an AI-powered analysis system and is intended 
        for informational purposes only. It should not be considered as medical advice, diagnosis, or treatment. 
        Always consult with qualified healthcare professionals for medical decisions. The information provided 
        is based on the lab values submitted and may not reflect your complete health status. Regular medical 
        check-ups and professional consultations are essential for proper healthcare management.
        """
        
        disclaimer_para = Paragraph(disclaimer_text, disclaimer_style)
        elements.append(disclaimer_para)
        
        # Footer text
        elements.append(Spacer(1, 0.2*inch))
        footer_text = "MedTech Early Risk Prediction System | AI-Powered Health Analytics"
        footer_para = Paragraph(footer_text, ParagraphStyle(
            name='Footer',
            parent=self.styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#9e9e9e'),
            alignment=TA_CENTER
        ))
        elements.append(footer_para)
        
        return elements


# Convenience function
def generate_medical_report_pdf(analysis_data: dict, patient_info: dict = None) -> BytesIO:
    """
    Generate a medical report PDF
    
    Args:
        analysis_data: Analysis results dictionary
        patient_info: Optional patient information
        
    Returns:
        BytesIO buffer containing the PDF
    """
    generator = MedicalReportPDFGenerator()
    return generator.generate_report(analysis_data, patient_info)
