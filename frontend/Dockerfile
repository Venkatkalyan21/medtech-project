# Build stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Runner stage
FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV production

# Copy standalone output and static files
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

# Expose port (Cloud Run uses PORT environment variable)
ENV PORT 3000
EXPOSE 3000

# Set the backend URL for the client-side (can be overridden at runtime)
# ENV NEXT_PUBLIC_API_URL http://localhost:8000

CMD ["node", "server.js"]
