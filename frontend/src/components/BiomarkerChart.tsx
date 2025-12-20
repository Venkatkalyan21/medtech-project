import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { motion } from 'framer-motion';
import styles from '../styles/BiomarkerChart.module.css';

interface BiomarkerData {
    name: string;
    value: number;
    normalMin: number;
    normalMax: number;
    unit: string;
}

interface BiomarkerChartProps {
    data: BiomarkerData[];
}

export default function BiomarkerChart({ data }: BiomarkerChartProps) {
    const getColor = (value: number, min: number, max: number) => {
        if (value < min || value > max) return '#ff4757';
        if (value < min * 1.1 || value > max * 0.9) return '#ffa502';
        return '#26de81';
    };

    return (
        <motion.div
            className={styles.container}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
        >
            <h3 className={styles.title}>Biomarker Analysis</h3>
            <p className={styles.subtitle}>Current values vs. normal ranges</p>

            <ResponsiveContainer width="100%" height={400}>
                <BarChart data={data} layout="vertical" margin={{ left: 100, right: 30 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                    <XAxis type="number" stroke="#a0aec0" />
                    <YAxis dataKey="name" type="category" stroke="#a0aec0" width={90} />
                    <Tooltip
                        contentStyle={{
                            backgroundColor: 'rgba(5, 5, 16, 0.95)',
                            border: '1px solid rgba(0, 243, 255, 0.3)',
                            borderRadius: '8px',
                            color: '#fff'
                        }}
                    />
                    <Bar dataKey="value" radius={[0, 8, 8, 0]}>
                        {data.map((entry, index) => (
                            <Cell
                                key={`cell-${index}`}
                                fill={getColor(entry.value, entry.normalMin, entry.normalMax)}
                            />
                        ))}
                    </Bar>
                </BarChart>
            </ResponsiveContainer>

            <div className={styles.legend}>
                <div className={styles.legendItem}>
                    <span className={styles.dot} style={{ backgroundColor: '#26de81' }}></span>
                    <span>Normal</span>
                </div>
                <div className={styles.legendItem}>
                    <span className={styles.dot} style={{ backgroundColor: '#ffa502' }}></span>
                    <span>Borderline</span>
                </div>
                <div className={styles.legendItem}>
                    <span className={styles.dot} style={{ backgroundColor: '#ff4757' }}></span>
                    <span>Abnormal</span>
                </div>
            </div>
        </motion.div>
    );
}
