import { useState } from 'react';
import styles from '../styles/DownloadButton.module.css';

interface DownloadButtonProps {
    analysisData: any;
    patientInfo?: {
        name?: string;
        age?: number;
        id?: string;
    };
    className?: string;
}

export default function DownloadButton({ analysisData, patientInfo, className }: DownloadButtonProps) {
    const [isDownloading, setIsDownloading] = useState(false);
    const [downloadStatus, setDownloadStatus] = useState<'idle' | 'success' | 'error'>('idle');

    const handleDownload = async () => {
        setIsDownloading(true);
        setDownloadStatus('idle');

        try {
            const response = await fetch('http://localhost:8000/download/pdf', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    analysis_data: analysisData,
                    patient_info: patientInfo || null
                }),
            });

            if (!response.ok) {
                throw new Error('Failed to generate PDF');
            }

            // Get the blob from response
            const blob = await response.blob();
            
            // Create download link
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            
            // Extract filename from Content-Disposition header or use default
            const contentDisposition = response.headers.get('Content-Disposition');
            let filename = 'medical_report.pdf';
            if (contentDisposition) {
                const filenameMatch = contentDisposition.match(/filename="?(.+)"?/);
                if (filenameMatch) {
                    filename = filenameMatch[1];
                }
            }
            
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            
            // Cleanup
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            
            setDownloadStatus('success');
            setTimeout(() => setDownloadStatus('idle'), 3000);
        } catch (error) {
            console.error('Error downloading PDF:', error);
            setDownloadStatus('error');
            setTimeout(() => setDownloadStatus('idle'), 3000);
        } finally {
            setIsDownloading(false);
        }
    };

    return (
        <button
            onClick={handleDownload}
            disabled={isDownloading}
            className={`${styles.downloadButton} ${className || ''} ${
                downloadStatus === 'success' ? styles.success : ''
            } ${downloadStatus === 'error' ? styles.error : ''}`}
        >
            <div className={styles.buttonContent}>
                {isDownloading ? (
                    <>
                        <div className={styles.spinner}></div>
                        <span>Generating PDF...</span>
                    </>
                ) : downloadStatus === 'success' ? (
                    <>
                        <svg className={styles.icon} viewBox="0 0 24 24" fill="none" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                        </svg>
                        <span>Downloaded!</span>
                    </>
                ) : downloadStatus === 'error' ? (
                    <>
                        <svg className={styles.icon} viewBox="0 0 24 24" fill="none" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                        <span>Error</span>
                    </>
                ) : (
                    <>
                        <svg className={styles.icon} viewBox="0 0 24 24" fill="none" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} 
                                d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                        <span>Download PDF Report</span>
                    </>
                )}
            </div>
            <div className={styles.glow}></div>
        </button>
    );
}
