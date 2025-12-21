# ==============================================================================
# GCP Deployment Script for Clinical Insights Platform (Windows/PowerShell)
# ==============================================================================

# User configuration
$PROJECT_ID = "my-login-project-481808"
$REGION = "us-central1"
$REPOSITORY = "medtech-images"
$MONGO_URI = "mongodb+srv://rahulrrk2807_db_user:axnU93xoK3bkFCnm@medtech.8rnmzbj.mongodb.net/?appName=medtech"
$GEMINI_API_KEY = "AIzaSyBICK4IOn5gJXn0l9n61OuHu3Ayc4ZLBKU"
$NEXTAUTH_SECRET = "f63c9a1d4b2e8f5a6c7d8e9f0a1b2c3d4"

$Root = $PSScriptRoot

Write-Host "----------------------------------------------------"
Write-Host "Step 1: Configuring Google Cloud Architecture..."
Write-Host "----------------------------------------------------"

# Enable Cloud Run and Artifact Registry
Write-Host "Enabling APIs..."
gcloud services enable run.googleapis.com artifactregistry.googleapis.com

# Create the Artifact Registry repository
Write-Host "Checking/Creating Artifact Registry repository: $REPOSITORY in $REGION..."
$repoList = gcloud artifacts repositories list --location=$REGION --filter="name:$REPOSITORY" --format="value(name)"
if (!$repoList) {
    Write-Host "Creating repository..."
    gcloud artifacts repositories create $REPOSITORY --repository-format=docker --location=$REGION --description="Docker repository for MedTech services"
    Write-Host "Waiting for repository propagation..."
    Start-Sleep -Seconds 10
}
else {
    Write-Host "Repository already exists."
}

# Authenticate Docker to GCP
Write-Host "Authenticating Docker to $REGION-docker.pkg.dev..."
gcloud auth configure-docker "$REGION-docker.pkg.dev" --quiet

Write-Host "`n----------------------------------------------------"
Write-Host "Step 2: Building and Pushing Backend..."
Write-Host "----------------------------------------------------"

Set-Location "$Root\backend"
$BACKEND_IMAGE = "$REGION-docker.pkg.dev/$PROJECT_ID/$REPOSITORY/backend:latest"
docker build --platform linux/amd64 -t $BACKEND_IMAGE .
docker push $BACKEND_IMAGE

Write-Host "`n----------------------------------------------------"
Write-Host "Step 3: Deploying Backend to Cloud Run..."
Write-Host "----------------------------------------------------"

gcloud run deploy medtech-backend `
    --image $BACKEND_IMAGE `
    --region $REGION `
    --platform managed `
    --allow-unauthenticated `
    --set-env-vars="MONGODB_URI=$MONGO_URI,GEMINI_API_KEY=$GEMINI_API_KEY"

# Capture the backend URL
$BACKEND_URL = gcloud run services describe medtech-backend --region $REGION --format='value(status.url)'
Write-Host "Backend deployed at: $BACKEND_URL" -ForegroundColor Green

Write-Host "`n----------------------------------------------------"
Write-Host "Step 4: Building and Pushing Frontend..."
Write-Host "----------------------------------------------------"

Set-Location "$Root\frontend"
$FRONTEND_IMAGE = "$REGION-docker.pkg.dev/$PROJECT_ID/$REPOSITORY/frontend:latest"
docker build --platform linux/amd64 -t $FRONTEND_IMAGE .
docker push $FRONTEND_IMAGE

Write-Host "`n----------------------------------------------------"
Write-Host "Step 5: Deploying Frontend to Cloud Run..."
Write-Host "----------------------------------------------------"

gcloud run deploy medtech-frontend `
    --image $FRONTEND_IMAGE `
    --region $REGION `
    --platform managed `
    --allow-unauthenticated `
    --set-env-vars="NEXT_PUBLIC_API_URL=$BACKEND_URL,NEXTAUTH_URL=http://localhost:3000,NEXTAUTH_SECRET=$NEXTAUTH_SECRET"

Write-Host "`n----------------------------------------------------"
Write-Host "DEPLOYMENT COMPLETE!" -ForegroundColor Green
Write-Host "----------------------------------------------------"
gcloud run services list
Set-Location $Root
