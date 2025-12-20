import React from 'react';
import { motion } from 'framer-motion';
import styles from '../styles/AIInsightsPanel.module.css';

interface Insight {
    type: 'positive' | 'warning' | 'critical';
    title: string;
    description: string;
}

interface AIInsightsPanelProps {
    insights: Insight[];
    recommendations: string[];
}

export default function AIInsightsPanel({ insights, recommendations }: AIInsightsPanelProps) {
    const getIcon = (type: string) => {
        switch (type) {
            case 'positive': return '✓';
            case 'warning': return '⚠';
            case 'critical': return '⚡';
            default: return '•';
        }
    };

    const getTypeClass = (type: string) => {
        switch (type) {
            case 'positive': return styles.positive;
            case 'warning': return styles.warning;
            case 'critical': return styles.critical;
            default: return '';
        }
    };

    return (
        <motion.div
            className={styles.container}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.4 }}
        >
            <div className={styles.header}>
                <h3 className={styles.title}>AI Health Insights</h3>
                <span className={styles.badge}>Powered by AI</span>
            </div>

            <div className={styles.section}>
                <h4 className={styles.sectionTitle}>Key Observations</h4>
                <div className={styles.insightsList}>
                    {insights.map((insight, index) => (
                        <motion.div
                            key={index}
                            className={`${styles.insightItem} ${getTypeClass(insight.type)}`}
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: 0.5 + index * 0.1 }}
                        >
                            <div className={styles.insightIcon}>{getIcon(insight.type)}</div>
                            <div className={styles.insightContent}>
                                <h5 className={styles.insightTitle}>{insight.title}</h5>
                                <p className={styles.insightDesc}>{insight.description}</p>
                            </div>
                        </motion.div>
                    ))}
                </div>
            </div>

            <div className={styles.section}>
                <h4 className={styles.sectionTitle}>Personalized Recommendations</h4>
                <ul className={styles.recommendationsList}>
                    {recommendations.map((rec, index) => (
                        <motion.li
                            key={index}
                            className={styles.recommendationItem}
                            initial={{ opacity: 0, x: -10 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: 0.7 + index * 0.1 }}
                        >
                            <span className={styles.bullet}>→</span>
                            {rec}
                        </motion.li>
                    ))}
                </ul>
            </div>
        </motion.div>
    );
}
