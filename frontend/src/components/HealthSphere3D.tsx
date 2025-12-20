import React, { useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { Sphere, MeshDistortMaterial } from '@react-three/drei';
import * as THREE from 'three';

interface HealthSphereProps {
    score: number; // 0-100
}

function AnimatedSphere({ score }: { score: number }) {
    const meshRef = useRef<THREE.Mesh>(null);

    useFrame((state) => {
        if (meshRef.current) {
            meshRef.current.rotation.x = state.clock.elapsedTime * 0.2;
            meshRef.current.rotation.y = state.clock.elapsedTime * 0.3;
        }
    });

    // Color based on score
    const getColor = () => {
        if (score < 30) return '#ff4757'; // Red - High risk
        if (score < 60) return '#ffa502'; // Orange - Moderate
        return '#26de81'; // Green - Low risk
    };

    return (
        <Sphere ref={meshRef} args={[1, 64, 64]}>
            <MeshDistortMaterial
                color={getColor()}
                attach="material"
                distort={0.4}
                speed={2}
                roughness={0.2}
                metalness={0.8}
                emissive={getColor()}
                emissiveIntensity={0.5}
            />
        </Sphere>
    );
}

export default function HealthSphere3D({ score }: HealthSphereProps) {
    return (
        <div style={{ width: '100%', height: '400px', position: 'relative' }}>
            <Canvas camera={{ position: [0, 0, 3], fov: 75 }}>
                <ambientLight intensity={0.5} />
                <pointLight position={[10, 10, 10]} intensity={1} />
                <pointLight position={[-10, -10, -10]} intensity={0.5} color="#00f3ff" />
                <AnimatedSphere score={score} />
            </Canvas>

            <div style={{
                position: 'absolute',
                bottom: '20px',
                left: '50%',
                transform: 'translateX(-50%)',
                textAlign: 'center',
                color: '#fff',
                zIndex: 10
            }}>
                <div style={{ fontSize: '3rem', fontWeight: 'bold', textShadow: '0 0 20px rgba(0,243,255,0.8)' }}>
                    {score}
                </div>
                <div style={{ fontSize: '1rem', color: '#a0aec0', marginTop: '0.5rem' }}>
                    Health Score
                </div>
            </div>
        </div>
    );
}
