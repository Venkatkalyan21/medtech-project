#!/bin/bash

# ==============================================================================
# 🚀 GCP Deployment Script for Clinical Insights Platform
# ==============================================================================

# User configuration (CHANGE THESE)
PROJECT_ID="my-login-project-481808"
REGION="us-central1"
REPOSITORY="medtech-images"
MONGO_URI="mongodb+srv://rahulrrk2807_db_user:axnU93xoK3bkFCnm@medtech.8rnmzbj.mongodb.net/?appName=medtech"
GEMINI_API_KEY="AIzaSyBICK4IOn5gJXn0l9n61OuHu3Ayc4ZLBKU"
NEXTAUTH_SECRET="f63c9a1d4b2e8f5a6c7d8e9f0a1b2c3d4"

echo "----------------------------------------------------"
echo "🛠️ Configuring Google Cloud Architecture..."
echo "----------------------------------------------------"

# Enable Cloud Run and Artifact Registry
gcloud services enable run.googleapis.com artifactregistry.googleapis.com

# Create the Artifact Registry repository
gcloud artifacts repositories create $REPOSITORY \
    --repository-format=docker \
    --location=$REGION \
    --description="Docker repository for MedTech services" || true

# Authenticate Docker to GCP
gcloud auth configure-docker $REGION-docker.pkg.dev

echo "----------------------------------------------------"
echo "📦 Building and Pushing Backend..."
echo "----------------------------------------------------"

cd backend
BACKEND_IMAGE="$REGION-docker.pkg.dev/$PROJECT_ID/$REPOSITORY/backend:latest"
docker build --platform linux/amd64 -t $BACKEND_IMAGE .
docker push $BACKEND_IMAGE

echo "----------------------------------------------------"
echo "🚀 Deploying Backend to Cloud Run..."
echo "----------------------------------------------------"

gcloud run deploy medtech-backend \
    --image $BACKEND_IMAGE \
    --region $REGION \
    --platform managed \
    --allow-unauthenticated \
    --set-env-vars="MONGODB_URI=$MONGO_URI,GEMINI_API_KEY=$GEMINI_API_KEY"

# Capture the backend URL
BACKEND_URL=$(gcloud run services describe medtech-backend --region $REGION --format='value(status.url)')
echo "✅ Backend deployed at: $BACKEND_URL"

echo "----------------------------------------------------"
echo "📦 Building and Pushing Frontend..."
echo "----------------------------------------------------"

cd ../frontend
FRONTEND_IMAGE="$REGION-docker.pkg.dev/$PROJECT_ID/$REPOSITORY/frontend:latest"
# Pass the Backend URL as a build time argument if needed, or set as runtime env
docker build --platform linux/amd64 -t $FRONTEND_IMAGE .
docker push $FRONTEND_IMAGE

echo "----------------------------------------------------"
echo "🚀 Deploying Frontend to Cloud Run..."
echo "----------------------------------------------------"

gcloud run deploy medtech-frontend \
    --image $FRONTEND_IMAGE \
    --region $REGION \
    --platform managed \
    --allow-unauthenticated \
    --set-env-vars="NEXT_PUBLIC_API_URL=$BACKEND_URL,NEXTAUTH_URL=http://localhost:3000,NEXTAUTH_SECRET=$NEXTAUTH_SECRET"

echo "----------------------------------------------------"
echo "🎉 DEPLOYMENT COMPLETE!"
echo "----------------------------------------------------"
gcloud run services list
