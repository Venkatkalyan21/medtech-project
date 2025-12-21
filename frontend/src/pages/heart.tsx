import { useState } from 'react';
import Head from 'next/head';
import { motion } from 'framer-motion';
import { predictHeart } from '../services/api';
import styles from '@/styles/Home.module.css'; // Reusing generic styles for now
import HolographicCard from '../components/HolographicCard';
import ParticleBackground from '../components/ParticleBackground';

export default function HeartPrediction() {
    const [formData, setFormData] = useState({
        age_years: 50,
        bmi: 25,
        ap_hi: 120,
        ap_lo: 80,
        cholesterol: 1,
        gluc: 1,
        smoke: 0,
        alco: 0,
        active: 1
    });
    const [result, setResult] = useState<any>(null);
    const [loading, setLoading] = useState(false);

    const handleChange = (e: any) => {
        setFormData({ ...formData, [e.target.name]: parseFloat(e.target.value) });
    };

    const handleSubmit = async (e: any) => {
        e.preventDefault();
        setLoading(true);
        try {
            const data = await predictHeart(formData);
            setResult(data);
        } catch (error) {
            console.error(error);
            alert("Prediction failed");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className={styles.container} style={{ minHeight: '100vh', padding: '2rem' }}>
            <Head>
                <title>Heart Disease Prediction</title>
            </Head>
            <ParticleBackground />

            <main style={{ maxWidth: '800px', margin: '0 auto', zIndex: 1, position: 'relative' }}>
                <h1 className="glow-text" style={{ textAlign: 'center', marginBottom: '2rem' }}>
                    Heart Disease Risk Analysis
                </h1>

                <HolographicCard>
                    <form onSubmit={handleSubmit} style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', padding: '1rem' }}>
                        <label>Age (years): <input name="age_years" type="number" value={formData.age_years} onChange={handleChange} className={styles.input} /></label>
                        <label>BMI: <input name="bmi" type="number" value={formData.bmi} onChange={handleChange} className={styles.input} /></label>
                        <label>Systolic BP: <input name="ap_hi" type="number" value={formData.ap_hi} onChange={handleChange} className={styles.input} /></label>
                        <label>Diastolic BP: <input name="ap_lo" type="number" value={formData.ap_lo} onChange={handleChange} className={styles.input} /></label>
                        <label>Cholesterol (1-3): <input name="cholesterol" type="number" value={formData.cholesterol} onChange={handleChange} className={styles.input} /></label>
                        <label>Glucose (1-3): <input name="gluc" type="number" value={formData.gluc} onChange={handleChange} className={styles.input} /></label>
                        <label>Smoke (0/1): <input name="smoke" type="number" value={formData.smoke} onChange={handleChange} className={styles.input} /></label>
                        <label>Alcohol (0/1): <input name="alco" type="number" value={formData.alco} onChange={handleChange} className={styles.input} /></label>
                        <label>Active (0/1): <input name="active" type="number" value={formData.active} onChange={handleChange} className={styles.input} /></label>

                        <div style={{ gridColumn: '1 / -1', marginTop: '1rem' }}>
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
                                {loading ? 'Analyzing...' : 'Analyze Risk'}
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
