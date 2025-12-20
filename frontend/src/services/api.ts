const API_URL = 'http://localhost:8000/api/v1';

export interface HealthReport {
    id: string;
    filename: string;
    uploadDate: string;
    status: 'analyzing' | 'completed' | 'failed';
}

export interface RiskAnalysis {
    riskScore: number; // 0-100
    riskLevel: 'Low' | 'Moderate' | 'High' | 'Critical';
    confidence: number;
    findings: string[];
    recommendations: string[];
    trends: {
        date: string;
        score: number;
    }[];
    biomarkers: {
        name: string;
        value: number;
        normalMin: number;
        normalMax: number;
        unit: string;
    }[];
    timeline: {
        date: string;
        overall: number;
        cardiovascular: number;
        metabolic: number;
        respiratory: number;
    }[];
    riskDistribution: {
        name: string;
        value: number;
        color: string;
    }[];
    vitalSigns: {
        metric: string;
        value: number;
        fullMark: number;
    }[];
    aiInsights: {
        type: 'positive' | 'warning' | 'critical';
        title: string;
        description: string;
    }[];
}

export const uploadReport = async (file: File): Promise<string> => {
    // In a real app, we would upload the file to the backend here.
    // For now, we'll simulate the upload and return a mock ID.

    // Simulating upload delay
    await new Promise(resolve => setTimeout(resolve, 1500));

    // Return a mock report ID
    return `RPT-${Math.floor(Math.random() * 10000)}`;
};

export const getAnalysis = async (reportId: string): Promise<RiskAnalysis> => {
    try {
        // Call the real backend API
        const response = await fetch(`${API_URL}/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                data: {
                    report_id: reportId,
                    // Pass any other necessary data here
                }
            }),
        });
        return {
            riskScore: 45,
            riskLevel: 'Moderate',
            confidence: 0.89,
            findings: [
                "Elevated LDL cholesterol levels detected.",
                "Slight irregularity in sleep patterns.",
                "Blood pressure trending upwards."
            ],
            recommendations: [
                "Reduce saturated fat intake.",
                "Aim for 7-8 hours of sleep.",
                "Monitor blood pressure daily."
            ],
            trends: [
                { date: '2023-01', score: 20 },
                { date: '2023-02', score: 25 },
                { date: '2023-03', score: 22 },
                { date: '2023-04', score: 30 },
                { date: '2023-05', score: 28 },
                { date: '2023-06', score: 45 },
            ],
            biomarkers: [
                { name: 'Cholesterol', value: 220, normalMin: 125, normalMax: 200, unit: 'mg/dL' },
                { name: 'Blood Sugar', value: 105, normalMin: 70, normalMax: 100, unit: 'mg/dL' },
                { name: 'Blood Pressure', value: 135, normalMin: 90, normalMax: 120, unit: 'mmHg' },
                { name: 'Heart Rate', value: 75, normalMin: 60, normalMax: 100, unit: 'bpm' },
                { name: 'BMI', value: 26, normalMin: 18.5, normalMax: 24.9, unit: 'kg/m²' },
                { name: 'Vitamin D', value: 25, normalMin: 30, normalMax: 100, unit: 'ng/mL' },
            ],
            timeline: [
                { date: 'Jan', overall: 65, cardiovascular: 70, metabolic: 60, respiratory: 75 },
                { date: 'Feb', overall: 68, cardiovascular: 72, metabolic: 63, respiratory: 77 },
                { date: 'Mar', overall: 70, cardiovascular: 75, metabolic: 65, respiratory: 78 },
                { date: 'Apr', overall: 72, cardiovascular: 76, metabolic: 68, respiratory: 80 },
                { date: 'May', overall: 75, cardiovascular: 78, metabolic: 72, respiratory: 82 },
                { date: 'Jun', overall: 78, cardiovascular: 80, metabolic: 75, respiratory: 85 },
            ],
            riskDistribution: [
                { name: 'Cardiovascular', value: 30, color: '#ff4757' },
                { name: 'Metabolic', value: 25, color: '#ffa502' },
                { name: 'Respiratory', value: 15, color: '#26de81' },
                { name: 'Neurological', value: 10, color: '#00f3ff' },
                { name: 'Other', value: 20, color: '#bc13fe' },
            ],
            vitalSigns: [
                { metric: 'Heart Rate', value: 75, fullMark: 100 },
                { metric: 'Blood Pressure', value: 68, fullMark: 100 },
                { metric: 'Oxygen Level', value: 95, fullMark: 100 },
                { metric: 'Temperature', value: 98, fullMark: 100 },
                { metric: 'Respiratory Rate', value: 85, fullMark: 100 },
                { metric: 'BMI', value: 72, fullMark: 100 },
            ],
            aiInsights: [
                {
                    type: 'positive',
                    title: 'Improving Trend',
                    description: 'Your overall health score has improved by 15% over the last 6 months.'
                },
                {
                    type: 'warning',
                    title: 'Cholesterol Levels',
                    description: 'LDL cholesterol is above normal range. Consider dietary changes and consult your doctor.'
                },
                {
                    type: 'warning',
                    title: 'Vitamin D Deficiency',
                    description: 'Your Vitamin D levels are below optimal. Increase sun exposure or consider supplements.'
                },
                {
                    type: 'critical',
                    title: 'Blood Pressure Alert',
                    description: 'Blood pressure is trending upwards. Monitor daily and schedule a check-up.'
                },
            ]
        };
    } catch (error) {
        console.error("Failed to fetch from backend, using mock data", error);
        // Return same mock data as above
        return {
            riskScore: 45,
            riskLevel: 'Moderate',
            confidence: 0.89,
            findings: [
                "Elevated LDL cholesterol levels detected.",
                "Slight irregularity in sleep patterns.",
                "Blood pressure trending upwards."
            ],
            recommendations: [
                "Reduce saturated fat intake.",
                "Aim for 7-8 hours of sleep.",
                "Monitor blood pressure daily."
            ],
            trends: [
                { date: '2023-01', score: 20 },
                { date: '2023-02', score: 25 },
                { date: '2023-03', score: 22 },
                { date: '2023-04', score: 30 },
                { date: '2023-05', score: 28 },
                { date: '2023-06', score: 45 },
            ],
            biomarkers: [
                { name: 'Cholesterol', value: 220, normalMin: 125, normalMax: 200, unit: 'mg/dL' },
                { name: 'Blood Sugar', value: 105, normalMin: 70, normalMax: 100, unit: 'mg/dL' },
                { name: 'Blood Pressure', value: 135, normalMin: 90, normalMax: 120, unit: 'mmHg' },
                { name: 'Heart Rate', value: 75, normalMin: 60, normalMax: 100, unit: 'bpm' },
                { name: 'BMI', value: 26, normalMin: 18.5, normalMax: 24.9, unit: 'kg/m²' },
                { name: 'Vitamin D', value: 25, normalMin: 30, normalMax: 100, unit: 'ng/mL' },
            ],
            timeline: [
                { date: 'Jan', overall: 65, cardiovascular: 70, metabolic: 60, respiratory: 75 },
                { date: 'Feb', overall: 68, cardiovascular: 72, metabolic: 63, respiratory: 77 },
                { date: 'Mar', overall: 70, cardiovascular: 75, metabolic: 65, respiratory: 78 },
                { date: 'Apr', overall: 72, cardiovascular: 76, metabolic: 68, respiratory: 80 },
                { date: 'May', overall: 75, cardiovascular: 78, metabolic: 72, respiratory: 82 },
                { date: 'Jun', overall: 78, cardiovascular: 80, metabolic: 75, respiratory: 85 },
            ],
            riskDistribution: [
                { name: 'Cardiovascular', value: 30, color: '#ff4757' },
                { name: 'Metabolic', value: 25, color: '#ffa502' },
                { name: 'Respiratory', value: 15, color: '#26de81' },
                { name: 'Neurological', value: 10, color: '#00f3ff' },
                { name: 'Other', value: 20, color: '#bc13fe' },
            ],
            vitalSigns: [
                { metric: 'Heart Rate', value: 75, fullMark: 100 },
                { metric: 'Blood Pressure', value: 68, fullMark: 100 },
                { metric: 'Oxygen Level', value: 95, fullMark: 100 },
                { metric: 'Temperature', value: 98, fullMark: 100 },
                { metric: 'Respiratory Rate', value: 85, fullMark: 100 },
                { metric: 'BMI', value: 72, fullMark: 100 },
            ],
            aiInsights: [
                {
                    type: 'positive',
                    title: 'Improving Trend',
                    description: 'Your overall health score has improved by 15% over the last 6 months.'
                },
                {
                    type: 'warning',
                    title: 'Cholesterol Levels',
                    description: 'LDL cholesterol is above normal range. Consider dietary changes and consult your doctor.'
                },
                {
                    type: 'warning',
                    title: 'Vitamin D Deficiency',
                    description: 'Your Vitamin D levels are below optimal. Increase sun exposure or consider supplements.'
                },
                {
                    type: 'critical',
                    title: 'Blood Pressure Alert',
                    description: 'Blood pressure is trending upwards. Monitor daily and schedule a check-up.'
                },
            ]
        };
    }
};
