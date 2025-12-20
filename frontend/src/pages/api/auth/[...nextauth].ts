import NextAuth from "next-auth";
import GoogleProvider from "next-auth/providers/google";
import CredentialsProvider from "next-auth/providers/credentials";

export default NextAuth({
    providers: [
        GoogleProvider({
            clientId: process.env.GOOGLE_CLIENT_ID || "",
            clientSecret: process.env.GOOGLE_CLIENT_SECRET || "",
        }),
        CredentialsProvider({
            name: "Credentials",
            credentials: {
                email: { label: "Email", type: "text" },
                password: { label: "Password", type: "password" }
            },
            async authorize(credentials) {
                // Mock authentication for demo purposes
                if (credentials?.email && credentials?.password) {
                    return { id: "1", name: "Dr. Smith", email: credentials.email };
                }
                return null;
            }
        })
    ],
    pages: {
        signIn: '/login',
    },
    theme: {
        colorScheme: "dark",
    },
});
