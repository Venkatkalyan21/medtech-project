import React from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { motion } from 'framer-motion';
import styles from '../styles/HealthTimeline.module.css';

interface TimelineData {
    date: string;
    overall: number;
    cardiovascular: number;
    metabolic: number;
    respiratory: number;
}

interface HealthTimelineProps {
    data: TimelineData[];
}

export default function HealthTimeline({ data }: HealthTimelineProps) {
    return (
        <motion.div
            className={styles.container}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
        >
            <h3 className={styles.title}>Health Score Timeline</h3>
            <p className={styles.subtitle}>Track your health metrics over time</p>

            <ResponsiveContainer width="100%" height={350}>
                <AreaChart data={data} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                    <defs>
                        <linearGradient id="colorOverall" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#00f3ff" stopOpacity={0.8} />
                            <stop offset="95%" stopColor="#00f3ff" stopOpacity={0} />
                        </linearGradient>
                        <linearGradient id="colorCardio" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#bc13fe" stopOpacity={0.8} />
                            <stop offset="95%" stopColor="#bc13fe" stopOpacity={0} />
                        </linearGradient>
                        <linearGradient id="colorMetabolic" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#26de81" stopOpacity={0.8} />
                            <stop offset="95%" stopColor="#26de81" stopOpacity={0} />
                        </linearGradient>
                        <linearGradient id="colorResp" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#ffa502" stopOpacity={0.8} />
                            <stop offset="95%" stopColor="#ffa502" stopOpacity={0} />
                        </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                    <XAxis dataKey="date" stroke="#a0aec0" />
                    <YAxis stroke="#a0aec0" domain={[0, 100]} />
                    <Tooltip
                        contentStyle={{
                            backgroundColor: 'rgba(5, 5, 16, 0.95)',
                            border: '1px solid rgba(0, 243, 255, 0.3)',
                            borderRadius: '8px',
                            color: '#fff'
                        }}
                    />
                    <Legend />
                    <Area
                        type="monotone"
                        dataKey="overall"
                        stroke="#00f3ff"
                        fillOpacity={1}
                        fill="url(#colorOverall)"
                        strokeWidth={2}
                    />
                    <Area
                        type="monotone"
                        dataKey="cardiovascular"
                        stroke="#bc13fe"
                        fillOpacity={1}
                        fill="url(#colorCardio)"
                        strokeWidth={2}
                    />
                    <Area
                        type="monotone"
                        dataKey="metabolic"
                        stroke="#26de81"
                        fillOpacity={1}
                        fill="url(#colorMetabolic)"
                        strokeWidth={2}
                    />
                    <Area
                        type="monotone"
                        dataKey="respiratory"
                        stroke="#ffa502"
                        fillOpacity={1}
                        fill="url(#colorResp)"
                        strokeWidth={2}
                    />
                </AreaChart>
            </ResponsiveContainer>
        </motion.div>
    );
}
