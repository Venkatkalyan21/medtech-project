import React, { useState } from 'react';
import { useRouter } from 'next/router';
import Head from 'next/head';
import { signIn } from 'next-auth/react';
import { motion } from 'framer-motion';
import ParticleBackground from '../components/ParticleBackground';
import HolographicCard from '../components/HolographicCard';
import styles from '@/styles/Login.module.css';


export default function Login() {
    const router = useRouter();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);

        const result = await signIn('credentials', {
            redirect: false,
            email,
            password,
        });

        if (result?.ok) {
            router.push('/upload');
        } else {
            setIsLoading(false);
            alert('Login failed');
        }
    };

    const handleGoogleLogin = () => {
        signIn('google', { callbackUrl: '/upload' });
    };

    return (
        <div className={styles.container}>
            <Head>
                <title>Login - Unmasking Silent Diseases</title>
            </Head>

            <ParticleBackground />

            <motion.div
                className={styles.content}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.8, type: 'spring' }}
            >
                <motion.div
                    className={styles.logo}
                    initial={{ y: -50, opacity: 0 }}
                    animate={{ y: 0, opacity: 1 }}
                    transition={{ delay: 0.2, duration: 0.6 }}
                >
                    <div className={styles.logoIcon}>🏥</div>
                    <h1 className={`${styles.logoText} glow-text`}>Unmasking Silent Diseases</h1>
                    <p className={styles.tagline}>AI-Powered Health Analytics</p>
                </motion.div>

                <HolographicCard delay={0.4}>
                    <div className={styles.cardContent}>
                        <h2 className={styles.title}>Welcome Back</h2>
                        <p className={styles.subtitle}>Access your health analytics dashboard</p>

                        <form onSubmit={handleLogin} className={styles.form}>
                            <div className={styles.inputGroup}>
                                <label htmlFor="email">Email Address</label>
                                <motion.input
                                    whileFocus={{ scale: 1.02 }}
                                    type="email"
                                    id="email"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    placeholder="doctor@hospital.com"
                                    required
                                    className={styles.input}
                                />
                            </div>

                            <div className={styles.inputGroup}>
                                <label htmlFor="password">Password</label>
                                <motion.input
                                    whileFocus={{ scale: 1.02 }}
                                    type="password"
                                    id="password"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    placeholder="••••••••"
                                    required
                                    className={styles.input}
                                />
                            </div>

                            <motion.button
                                whileHover={{ scale: 1.05 }}
                                whileTap={{ scale: 0.95 }}
                                type="submit"
                                className={styles.button}
                                disabled={isLoading}
                            >
                                {isLoading ? (
                                    <span className={styles.loading}>
                                        <span className={styles.spinner}></span>
                                        Authenticating...
                                    </span>
                                ) : (
                                    'Access Dashboard'
                                )}
                            </motion.button>
                        </form>

                        <div className={styles.divider}>
                            <span>OR</span>
                        </div>

                        <motion.button
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                            type="button"
                            className={styles.googleButton}
                            onClick={handleGoogleLogin}
                        >
                            <img
                                src="https://www.svgrepo.com/show/475656/google-color.svg"
                                alt="Google"
                                width="20"
                                height="20"
                            />
                            Sign in with Google
                        </motion.button>

                        <div className={styles.footer}>
                            <p>Don't have an account? <a href="#">Request Access</a></p>
                        </div>
                    </div>
                </HolographicCard>

                <motion.div
                    className={styles.features}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.6, duration: 0.6 }}
                >
                    <div className={styles.feature}>
                        <span className={styles.featureIcon}>🔒</span>
                        <span>Secure & Encrypted</span>
                    </div>
                    <div className={styles.feature}>
                        <span className={styles.featureIcon}>🤖</span>
                        <span>AI-Powered Analysis</span>
                    </div>
                    <div className={styles.feature}>
                        <span className={styles.featureIcon}>📊</span>
                        <span>Real-time Insights</span>
                    </div>
                </motion.div>
            </motion.div>
        </div>
    );
}
