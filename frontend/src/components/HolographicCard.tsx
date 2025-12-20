import React, { ReactNode } from 'react';
import { motion } from 'framer-motion';
import styles from '../styles/HolographicCard.module.css';

interface HolographicCardProps {
    children: ReactNode;
    delay?: number;
}

export default function HolographicCard({ children, delay = 0 }: HolographicCardProps) {
    const [mousePosition, setMousePosition] = React.useState({ x: 0, y: 0 });

    const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
        const rect = e.currentTarget.getBoundingClientRect();
        const x = (e.clientX - rect.left) / rect.width;
        const y = (e.clientY - rect.top) / rect.height;
        setMousePosition({ x, y });
    };

    return (
        <motion.div
            className={styles.card}
            initial={{ opacity: 0, y: 50, rotateX: -15 }}
            animate={{ opacity: 1, y: 0, rotateX: 0 }}
            transition={{ duration: 0.8, delay, type: 'spring', stiffness: 100 }}
            onMouseMove={handleMouseMove}
            onMouseLeave={() => setMousePosition({ x: 0.5, y: 0.5 })}
            style={{
                transform: `perspective(1000px) rotateX(${(mousePosition.y - 0.5) * 10}deg) rotateY(${(mousePosition.x - 0.5) * -10}deg)`,
            }}
        >
            <div className={styles.holographicOverlay} />
            <div className={styles.glowEffect} />
            <div className={styles.content}>
                {children}
            </div>
        </motion.div>
    );
}
