import { useState } from 'react';
import Head from 'next/head';
import { motion } from 'framer-motion';
import { predictFitbit } from '../services/api';
import styles from '@/styles/Home.module.css';
import HolographicCard from '../components/HolographicCard';
import ParticleBackground from '../components/ParticleBackground';

export default function FitbitPrediction() {
    const [jsonInput, setJsonInput] = useState('');
    const [result, setResult] = useState<any>(null);
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e: any) => {
        e.preventDefault();
        setLoading(true);
        try {
            let data;
            try {
                data = JSON.parse(jsonInput);
            } catch (err) {
                alert("Invalid JSON format");
                setLoading(false);
                return;
            }

            const response = await predictFitbit(data);
            setResult(response);
        } catch (error) {
            console.error(error);
            alert("Prediction failed");
        } finally {
            setLoading(false);
        }
    };

    const loadSample = () => {
        const sample = {
            "TotalSteps": 10000,
            "TotalDistance": 8.0,
            "TrackerDistance": 8.0,
            "LoggedActivitiesDistance": 0,
            "VeryActiveDistance": 4.0,
            "ModeratelyActiveDistance": 2.0,
            "LightActiveDistance": 2.0,
            "SedentaryActiveDistance": 0,
            "VeryActiveMinutes": 60,
            "FairlyActiveMinutes": 30,
            "LightlyActiveMinutes": 200,
            "SedentaryMinutes": 500,
            "Calories": 2500,
            "TotalSleepRecords": 1,
            "TotalMinutesAsleep": 400,
            "TotalTimeInBed": 450,
            "date": "2024-01-01"
        };
        setJsonInput(JSON.stringify(sample, null, 2));
    };

    return (
        <div className={styles.container} style={{ minHeight: '100vh', padding: '2rem' }}>
            <Head>
                <title>Fitbit Anomaly Detection</title>
            </Head>
            <ParticleBackground />

            <main style={{ maxWidth: '800px', margin: '0 auto', zIndex: 1, position: 'relative' }}>
                <h1 className="glow-text" style={{ textAlign: 'center', marginBottom: '2rem' }}>
                    Fitbit Activity Analysis
                </h1>

                <HolographicCard>
                    <div style={{ marginBottom: '1rem' }}>
                        <p>Paste your Fitbit daily activity JSON here or <button onClick={loadSample} style={{ background: 'none', border: 'none', color: '#00f3ff', cursor: 'pointer', textDecoration: 'underline' }}>load sample</button>.</p>
                    </div>
                    <form onSubmit={handleSubmit}>
                        <textarea
                            value={jsonInput}
                            onChange={(e) => setJsonInput(e.target.value)}
                            rows={15}
                            style={{ width: '100%', background: 'rgba(0,0,0,0.5)', color: 'white', border: '1px solid #333', borderRadius: '8px', padding: '1rem', fontFamily: 'monospace' }}
                            placeholder='{"TotalSteps": 10000, ...}'
                        />

                        <div style={{ marginTop: '1rem' }}>
                            <button type="submit" disabled={loading} style={{
                                width: '100%',
                                padding: '1rem',
                                background: 'linear-gradient(45deg, #00f3ff, #bc13fe)',
                                border: 'none',
                                borderRadius: '8px',
                                color: 'white',
                                fontWeight: 'bold',
                                cursor: 'pointer'
                            }}>
                                {loading ? 'Analyzing...' : 'Detect Anomalies'}
                            </button>
                        </div>
                    </form>
                </HolographicCard>

                {result && (
                    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} style={{ marginTop: '2rem' }}>
                        <HolographicCard>
                            <h2 style={{ textAlign: 'center', color: result.is_anomaly ? '#ff4757' : '#26de81' }}>
                                Result: {result.status}
                            </h2>
                            <p style={{ textAlign: 'center' }}>Anomaly Score: {result.score.toFixed(4)}</p>
                        </HolographicCard>
                    </motion.div>
                )}
            </main>
        </div>
    );
}
