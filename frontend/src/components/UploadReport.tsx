import React, { useState, useCallback } from 'react';
import { uploadReport } from '../services/api';
import styles from '../styles/UploadReport.module.css';

interface UploadReportProps {
    onUploadComplete: (reportId: string) => void;
}

export default function UploadReport({ onUploadComplete }: UploadReportProps) {
    const [isDragging, setIsDragging] = useState(false);
    const [isUploading, setIsUploading] = useState(false);

    const handleDragOver = useCallback((e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(true);
    }, []);

    const handleDragLeave = useCallback((e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(false);
    }, []);

    const handleDrop = useCallback(async (e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(false);

        const files = e.dataTransfer.files;
        if (files.length > 0) {
            await handleUpload(files[0]);
        }
    }, []);

    const handleFileSelect = useCallback(async (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files.length > 0) {
            await handleUpload(e.target.files[0]);
        }
    }, []);

    const handleUpload = async (file: File) => {
        setIsUploading(true);
        try {
            const reportId = await uploadReport(file);
            onUploadComplete(reportId);
        } catch (error) {
            console.error('Upload failed:', error);
            alert('Upload failed. Please try again.');
        } finally {
            setIsUploading(false);
        }
    };

    return (
        <div
            className={`${styles.dropzone} ${isDragging ? styles.dragging : ''}`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
        >
            <input
                type="file"
                id="fileInput"
                className={styles.fileInput}
                onChange={handleFileSelect}
                accept=".pdf,.jpg,.png,.csv"
            />
            <label htmlFor="fileInput" className={styles.label}>
                {isUploading ? (
                    <div className={styles.uploading}>
                        <div className={styles.spinner}></div>
                        <p>Analyzing health data...</p>
                    </div>
                ) : (
                    <>
                        <div className={styles.icon}>📄</div>
                        <p className={styles.text}>Drag & Drop your health report here</p>
                        <p className={styles.subtext}>or click to browse (PDF, JPG, CSV)</p>
                    </>
                )}
            </label>
        </div>
    );
}
