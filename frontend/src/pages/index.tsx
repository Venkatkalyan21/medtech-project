import { useEffect } from "react";
import { useRouter } from "next/router";
import Head from "next/head";

export default function Home() {
    const router = useRouter();

    useEffect(() => {
        // Redirect to login page immediately
        router.push('/login');
    }, [router]);

    return (
        <div>
            <Head>
                <title>Early Risk Prediction</title>
                <meta name="description" content="AI-Driven Early Risk Prediction System" />
            </Head>
            <p>Redirecting to login...</p>
        </div>
    );
}
