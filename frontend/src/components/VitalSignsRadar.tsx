import React from 'react';
import { RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, ResponsiveContainer, Legend, Tooltip } from 'recharts';
import { motion } from 'framer-motion';
import styles from '../styles/VitalSignsRadar.module.css';

interface VitalData {
    metric: string;
    value: number;
    fullMark: number;
}

interface VitalSignsRadarProps {
    data: VitalData[];
}

export default function VitalSignsRadar({ data }: VitalSignsRadarProps) {
    return (
        <motion.div
            className={styles.container}
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5, delay: 0.3 }}
        >
            <h3 className={styles.title}>Vital Signs Overview</h3>
            <p className={styles.subtitle}>Comprehensive health metrics at a glance</p>

            <ResponsiveContainer width="100%" height={350}>
                <RadarChart data={data}>
                    <PolarGrid stroke="rgba(255,255,255,0.2)" />
                    <PolarAngleAxis
                        dataKey="metric"
                        stroke="#a0aec0"
                        tick={{ fill: '#a0aec0', fontSize: 12 }}
                    />
                    <PolarRadiusAxis
                        angle={90}
                        domain={[0, 100]}
                        stroke="#a0aec0"
                    />
                    <Radar
                        name="Current Values"
                        dataKey="value"
                        stroke="#00f3ff"
                        fill="#00f3ff"
                        fillOpacity={0.6}
                        strokeWidth={2}
                    />
                    <Tooltip
                        contentStyle={{
                            backgroundColor: 'rgba(5, 5, 16, 0.95)',
                            border: '1px solid rgba(0, 243, 255, 0.3)',
                            borderRadius: '8px',
                            color: '#fff'
                        }}
                    />
                    <Legend />
                </RadarChart>
            </ResponsiveContainer>
        </motion.div>
    );
}
