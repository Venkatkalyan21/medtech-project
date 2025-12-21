import { useState } from 'react';
import Head from 'next/head';
import { motion } from 'framer-motion';
import { predictCKD } from '../services/api';
import styles from '@/styles/Home.module.css';
import HolographicCard from '../components/HolographicCard';
import ParticleBackground from '../components/ParticleBackground';

export default function CKDPrediction() {
    const [formData, setFormData] = useState({
        age: 48, al: 0, ane: "no", appet: "good", ba: "notpresent", bgr: 120,
        bp: 80, bu: 36, cad: "no", dm: "no", htn: "no", pc: "normal",
        pcc: "notpresent", pe: "no", pot: 4.4, rbc: "normal", sg: 1.020, sod: 138, su: 0
    });
    const [result, setResult] = useState<any>(null);
    const [loading, setLoading] = useState(false);

    const handleChange = (e: any) => {
        const value = e.target.type === 'number' ? parseFloat(e.target.value) : e.target.value;
        setFormData({ ...formData, [e.target.name]: value });
    };

    const handleSubmit = async (e: any) => {
        e.preventDefault();
        setLoading(true);
        try {
            const data = await predictCKD(formData);
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
                <title>CKD Prediction</title>
            </Head>
            <ParticleBackground />

            <main style={{ maxWidth: '800px', margin: '0 auto', zIndex: 1, position: 'relative' }}>
                <h1 className="glow-text" style={{ textAlign: 'center', marginBottom: '2rem' }}>
                    Kidney Disease Prediction
                </h1>

                <HolographicCard>
                    <form onSubmit={handleSubmit} style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', padding: '1rem' }}>
                        <label>Age: <input name="age" type="number" value={formData.age} onChange={handleChange} className={styles.input} /></label>
                        <label>Blood Pressure: <input name="bp" type="number" value={formData.bp} onChange={handleChange} className={styles.input} /></label>
                        <label>Specific Gravity: <input name="sg" type="number" step="0.005" value={formData.sg} onChange={handleChange} className={styles.input} /></label>
                        <label>Albumin (0-5): <input name="al" type="number" value={formData.al} onChange={handleChange} className={styles.input} /></label>
                        <label>Sugar (0-5): <input name="su" type="number" value={formData.su} onChange={handleChange} className={styles.input} /></label>
                        <label>Red Blood Cells:
                            <select name="rbc" value={formData.rbc} onChange={handleChange} className={styles.input}>
                                <option value="normal">Normal</option>
                                <option value="abnormal">Abnormal</option>
                            </select>
                        </label>
                        <label>Pus Cell:
                            <select name="pc" value={formData.pc} onChange={handleChange} className={styles.input}>
                                <option value="normal">Normal</option>
                                <option value="abnormal">Abnormal</option>
                            </select>
                        </label>
                        <label>Pus Cell Clumps:
                            <select name="pcc" value={formData.pcc} onChange={handleChange} className={styles.input}>
                                <option value="notpresent">Not Present</option>
                                <option value="present">Present</option>
                            </select>
                        </label>
                        <label>Bacteria:
                            <select name="ba" value={formData.ba} onChange={handleChange} className={styles.input}>
                                <option value="notpresent">Not Present</option>
                                <option value="present">Present</option>
                            </select>
                        </label>
                        <label>Blood Glucose Random: <input name="bgr" type="number" value={formData.bgr} onChange={handleChange} className={styles.input} /></label>
                        <label>Blood Urea: <input name="bu" type="number" value={formData.bu} onChange={handleChange} className={styles.input} /></label>
                        <label>Serum Creatinine: <input name="sc" type="number" disabled placeholder="(Ignored)" className={styles.input} style={{ opacity: 0.5 }} /></label>
                        <label>Sodium: <input name="sod" type="number" value={formData.sod} onChange={handleChange} className={styles.input} /></label>
                        <label>Potassium: <input name="pot" type="number" value={formData.pot} onChange={handleChange} className={styles.input} /></label>
                        <label>Hemoglobin: <input name="hemo" type="number" disabled placeholder="(Ignored)" className={styles.input} style={{ opacity: 0.5 }} /></label>
                        <label>Packed Cell Volume: <input name="pcv" type="number" disabled placeholder="(Ignored)" className={styles.input} style={{ opacity: 0.5 }} /></label>

                        <label>Hypertension: <select name="htn" value={formData.htn} onChange={handleChange} className={styles.input}><option value="no">No</option><option value="yes">Yes</option></select></label>
                        <label>Diabetes Mellitus: <select name="dm" value={formData.dm} onChange={handleChange} className={styles.input}><option value="no">No</option><option value="yes">Yes</option></select></label>
                        <label>Coronary Artery Disease: <select name="cad" value={formData.cad} onChange={handleChange} className={styles.input}><option value="no">No</option><option value="yes">Yes</option></select></label>
                        <label>Appetite: <select name="appet" value={formData.appet} onChange={handleChange} className={styles.input}><option value="good">Good</option><option value="poor">Poor</option></select></label>
                        <label>Pedal Edema: <select name="pe" value={formData.pe} onChange={handleChange} className={styles.input}><option value="no">No</option><option value="yes">Yes</option></select></label>
                        <label>Anemia: <select name="ane" value={formData.ane} onChange={handleChange} className={styles.input}><option value="no">No</option><option value="yes">Yes</option></select></label>

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
                                {loading ? 'Analyzing...' : 'Predict CKD Risk'}
                            </button>
                        </div>
                    </form>
                </HolographicCard>

                {result && (
                    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} style={{ marginTop: '2rem' }}>
                        <HolographicCard>
                            <h2 style={{ textAlign: 'center', color: result.is_ckd ? '#ff4757' : '#26de81' }}>
                                Result: {result.is_ckd ? 'Likely CKD' : 'No CKD Detected'}
                            </h2>
                            <p style={{ textAlign: 'center' }}>Confidence: {(result.probability * 100).toFixed(1)}%</p>
                        </HolographicCard>
                    </motion.div>
                )}
            </main>
        </div>
    );
}
