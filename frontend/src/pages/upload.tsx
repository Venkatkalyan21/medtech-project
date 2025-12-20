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
                <title>Upload Report - Unmasking Silent Diseases</title>
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
                </div>
            </main>
        </div>
    );
}
