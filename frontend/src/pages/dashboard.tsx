import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import Head from 'next/head';
import { motion, AnimatePresence } from 'framer-motion';
import { getAnalysis, RiskAnalysis } from '../services/api';
import RiskMeter3D from '../components/RiskMeter3D';
import TrendChart from '../components/TrendChart';
import ReasoningPanel from '../components/ReasoningPanel';
import ConfidenceMeter from '../components/ConfidenceMeter';
import BiomarkerChart from '../components/BiomarkerChart';
import HealthTimeline from '../components/HealthTimeline';
import RiskDistribution from '../components/RiskDistribution';
import VitalSignsRadar from '../components/VitalSignsRadar';
import AIInsightsPanel from '../components/AIInsightsPanel';
import ParticleBackground from '../components/ParticleBackground';
import HolographicCard from '../components/HolographicCard';
import HealthSphere3D from '../components/HealthSphere3D';
import DownloadButton from '../components/DownloadButton';
import styles from '@/styles/Dashboard.module.css';

export default function Dashboard() {
    const router = useRouter();
    const { reportId } = router.query;
    const [analysis, setAnalysis] = useState<RiskAnalysis | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (reportId) {
            getAnalysis(reportId as string).then(data => {
                setAnalysis(data);
                setLoading(false);
            });
        }
    }, [reportId]);

    if (loading) {
        return (
            <div className={styles.loading}>
                <ParticleBackground />
                <motion.div
                    initial={{ scale: 0 }}
                    animate={{ scale: 1, rotate: 360 }}
                    transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                    className={styles.spinner}
                ></motion.div>
                <motion.p
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.5 }}
                    className="glow-text"
                >
                    Generating comprehensive health insights...
                </motion.p>
            </div>
        );
    }

    if (!analysis) return null;

    return (
        <div className={styles.container}>
            <Head>
                <title>Dashboard | Clinical Insights Platform</title>
            </Head>

            <ParticleBackground />

            <AnimatePresence>
                <motion.header
                    className={styles.header}
                    initial={{ opacity: 0, y: -50 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8, type: 'spring' }}
                >
                    <div>
                        <h1 className="professional-title">Clinical Health Analytics</h1>
                        <p className={styles.subtitle}>Comprehensive AI-powered health insights with 3D visualization</p>
                    </div>
                    <div className={styles.meta}>
                        <span className={styles.reportId}>Report ID: {reportId}</span>
                        <ConfidenceMeter score={analysis.confidence} />
                        <DownloadButton
                            analysisData={analysis}
                            patientInfo={{
                                id: reportId as string
                            }}
                        />
                    </div>
                </motion.header>

                <main className={styles.dashboardGrid}>
                    {/* Row 1: 3D Health Sphere and AI Insights */}
                    <HolographicCard delay={0.1}>
                        <HealthSphere3D score={100 - analysis.riskScore} />
                    </HolographicCard>

                    <HolographicCard delay={0.2}>
                        <AIInsightsPanel
                            insights={analysis.aiInsights}
                            recommendations={analysis.recommendations}
                        />
                    </HolographicCard>

                    {/* Row 2: Biomarker Chart (Full Width) */}
                    <div className={styles.biomarkerSection}>
                        <HolographicCard delay={0.3}>
                            <BiomarkerChart data={analysis.biomarkers} />
                        </HolographicCard>
                    </div>

                    {/* Row 3: Health Timeline (Full Width) */}
                    <div className={styles.timelineSection}>
                        <HolographicCard delay={0.4}>
                            <HealthTimeline data={analysis.timeline} />
                        </HolographicCard>
                    </div>

                    {/* Row 4: Risk Distribution and Vital Signs */}
                    <HolographicCard delay={0.5}>
                        <RiskDistribution data={analysis.riskDistribution} />
                    </HolographicCard>

                    <HolographicCard delay={0.6}>
                        <VitalSignsRadar data={analysis.vitalSigns} />
                    </HolographicCard>

                    {/* Row 5: Trend Chart and Reasoning Panel */}
                    <HolographicCard delay={0.7}>
                        <TrendChart data={analysis.trends} />
                    </HolographicCard>

                    <HolographicCard delay={0.8}>
                        <ReasoningPanel
                            findings={analysis.findings}
                            recommendations={analysis.recommendations}
                        />
                    </HolographicCard>
                </main>
            </AnimatePresence>
        </div>
    );
}
