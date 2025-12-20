import React from 'react';
import styles from '../styles/ConfidenceMeter.module.css';

interface ConfidenceMeterProps {
    score: number; // 0-1
}

export default function ConfidenceMeter({ score }: ConfidenceMeterProps) {
    const percentage = Math.round(score * 100);

    return (
        <div className={styles.container}>
            <div className={styles.header}>
                <span className={styles.label}>AI Confidence</span>
                <span className={styles.value}>{percentage}%</span>
            </div>
            <div className={styles.track}>
                <div
                    className={styles.bar}
                    style={{ width: `${percentage}%` }}
                ></div>
            </div>
        </div>
    );
}
