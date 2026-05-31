# ==============================================================================
# GCP Deployment Script for Clinical Insights Platform (Windows/PowerShell)
# ==============================================================================

# User configuration
$PROJECT_ID = "my-login-project-481808"
$REGION = "us-central1"
$REPOSITORY = "medtech-images"

# Use environment variables for sensitive data
$MONGO_URI = $env:MONGO_URI
$GEMINI_API_KEY = $env:GEMINI_API_KEY
$NEXTAUTH_SECRET = $env:NEXTAUTH_SECRET

# Check if required env vars are set
if ([string]::IsNullOrEmpty($MONGO_URI) -or [string]::IsNullOrEmpty($GEMINI_API_KEY) -or [string]::IsNullOrEmpty($NEXTAUTH_SECRET)) {
    Write-Host "❌ Error: Missing required environment variables!" -ForegroundColor Red
    Write-Host "Please set: MONGO_URI, GEMINI_API_KEY, NEXTAUTH_SECRET" -ForegroundColor Red
    exit 1
}

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
if (!$BACKEND_URL) {
    Write-Host "ERROR: Backend deployment failed or URL could not be retrieved. Stopping." -ForegroundColor Red
    exit 1
}
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

# Initial deployment to get the URL
gcloud run deploy medtech-frontend `
    --image $FRONTEND_IMAGE `
    --region $REGION `
    --platform managed `
    --allow-unauthenticated `
    --set-env-vars="NEXT_PUBLIC_API_URL=$BACKEND_URL,NEXTAUTH_URL=http://temp.url,NEXTAUTH_SECRET=$NEXTAUTH_SECRET"

# Capture the frontend URL
$FRONTEND_URL = gcloud run services describe medtech-frontend --region $REGION --format='value(status.url)'
Write-Host "Frontend URL captured: $FRONTEND_URL" -ForegroundColor Green

# Update the frontend with the correct NEXTAUTH_URL for production
Write-Host "Updating Frontend with production NEXTAUTH_URL..."
gcloud run services update medtech-frontend `
    --region $REGION `
    --set-env-vars="NEXT_PUBLIC_API_URL=$BACKEND_URL,NEXTAUTH_URL=$FRONTEND_URL,NEXTAUTH_SECRET=$NEXTAUTH_SECRET"

Write-Host "`n----------------------------------------------------"
Write-Host "DEPLOYMENT COMPLETE!" -ForegroundColor Green
Write-Host "----------------------------------------------------"
Write-Host "FRONTEND: $FRONTEND_URL" -ForegroundColor Cyan
Write-Host "BACKEND:  $BACKEND_URL" -ForegroundColor Cyan
Set-Location $Root
