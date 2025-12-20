import React from 'react';
import styles from '../styles/RiskMeter3D.module.css';

interface RiskMeterProps {
    score: number;
    level: string;
}

export default function RiskMeter3D({ score, level }: RiskMeterProps) {
    const rotation = (score / 100) * 180;

    return (
        <div className={styles.container}>
            <div className={styles.gauge}>
                <div className={styles.mask}>
                    <div className={styles.semiCircle}></div>
                    <div
                        className={styles.needle}
                        style={{ transform: `rotate(${rotation}deg)` }}
                    ></div>
                </div>
            </div>
            <div className={styles.info}>
                <h3 className={styles.score}>{score}</h3>
                <p className={styles.level} data-level={level}>{level} Risk</p>
            </div>
        </div>
    );
}
