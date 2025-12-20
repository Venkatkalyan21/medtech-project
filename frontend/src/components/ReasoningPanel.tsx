import React from 'react';
import styles from '../styles/ReasoningPanel.module.css';

interface ReasoningPanelProps {
    findings: string[];
    recommendations: string[];
}

export default function ReasoningPanel({ findings, recommendations }: ReasoningPanelProps) {
    return (
        <div className={styles.container}>
            <div className={styles.section}>
                <h3 className={styles.title}>Key Findings</h3>
                <ul className={styles.list}>
                    {findings.map((finding, idx) => (
                        <li key={idx} className={styles.item}>
                            <span className={styles.bullet}>•</span>
                            {finding}
                        </li>
                    ))}
                </ul>
            </div>
            <div className={styles.section}>
                <h3 className={styles.title}>Recommendations</h3>
                <ul className={styles.list}>
                    {recommendations.map((rec, idx) => (
                        <li key={idx} className={styles.item}>
                            <span className={styles.bullet}>✓</span>
                            {rec}
                        </li>
                    ))}
                </ul>
            </div>
        </div>
    );
}
