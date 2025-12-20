import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import styles from '../styles/TrendChart.module.css';

interface TrendData {
    date: string;
    score: number;
}

interface TrendChartProps {
    data: TrendData[];
}

export default function TrendChart({ data }: TrendChartProps) {
    return (
        <div className={styles.container}>
            <h3 className={styles.title}>Health Trends</h3>
            <div className={styles.chartWrapper}>
                <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={data}>
                        <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                        <XAxis dataKey="date" stroke="#a0aec0" />
                        <YAxis stroke="#a0aec0" />
                        <Tooltip
                            contentStyle={{
                                backgroundColor: 'rgba(5, 5, 16, 0.9)',
                                border: '1px solid rgba(255,255,255,0.1)',
                                borderRadius: '0.5rem',
                                color: '#fff'
                            }}
                        />
                        <Line
                            type="monotone"
                            dataKey="score"
                            stroke="#00f3ff"
                            strokeWidth={3}
                            dot={{ r: 4, fill: '#00f3ff', strokeWidth: 2, stroke: '#fff' }}
                            activeDot={{ r: 6, fill: '#bc13fe' }}
                        />
                    </LineChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
}
