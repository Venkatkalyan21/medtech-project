import { useRouter } from 'next/router';
import Head from 'next/head';
import UploadReport from '../components/UploadReport';
import styles from '@/styles/Home.module.css'; // Reusing layout styles

export default function Upload() {
    const router = useRouter();

    const handleUploadComplete = (reportId: string) => {
        // Navigate to dashboard with report ID
        router.push(`/dashboard?reportId=${reportId}`);
    };

    return (
        <div className={styles.container}>
            <Head>
                <title>Upload | Clinical Insights Platform</title>
            </Head>

            <main className={styles.main}>
                <h1 className={styles.title} style={{ fontSize: '2.5rem' }}>
                    Upload Your Health Data
                </h1>
                <p className={styles.description}>
                    Securely upload your lab reports or connect your wearable data for analysis.
                </p>

                <div style={{ width: '100%', maxWidth: '600px' }}>
                    <UploadReport onUploadComplete={handleUploadComplete} />

                    <div style={{ marginTop: '3rem', borderTop: '1px solid #333', paddingTop: '1rem' }}>
                        <h3 className="professional-title" style={{ textAlign: 'center', marginBottom: '1rem', backgroundClip: 'text', WebkitBackgroundClip: 'text' }}>Quick Tools</h3>
                        <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center', flexWrap: 'wrap' }}>
                            <button onClick={() => router.push('/heart')} className={styles.button} style={{ padding: '0.8rem 1.5rem', background: 'rgba(0,0,0,0.5)', border: '1px solid #00f3ff', color: '#00f3ff', borderRadius: '20px', cursor: 'pointer' }}>
                                Heart Analysis
                            </button>
                            <button onClick={() => router.push('/ckd')} className={styles.button} style={{ padding: '0.8rem 1.5rem', background: 'rgba(0,0,0,0.5)', border: '1px solid #bc13fe', color: '#bc13fe', borderRadius: '20px', cursor: 'pointer' }}>
                                CKD Prediction
                            </button>
                            <button onClick={() => router.push('/fitbit')} className={styles.button} style={{ padding: '0.8rem 1.5rem', background: 'rgba(0,0,0,0.5)', border: '1px solid #26de81', color: '#26de81', borderRadius: '20px', cursor: 'pointer' }}>
                                Fitbit Activity
                            </button>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    );
}
