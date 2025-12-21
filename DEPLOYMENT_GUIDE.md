# 🌐 Google Cloud Deployment Guide

Follow these steps to deploy your **Clinical Insights Platform** to Google Cloud using your free credits.

## 1. Prerequisites
- **Google Cloud SDK**: Install it on your machine ([Guide](https://cloud.google.com/sdk/docs/install)).
- **Docker**: Must be installed and running.
- **MongoDB Atlas**: Create a free cluster and get your connection string ([Atlas](https://www.mongodb.com/cloud/atlas/register)).

## 2. Set Up Google Cloud
1.  Open your terminal and login:
    ```bash
    gcloud auth login
    ```
2.  Set your Project ID:
    ```bash
    gcloud config set project [YOUR_PROJECT_ID]
    ```

## 3. Configure and Run Deployment
1.  Edit the `deploy.sh` file in the project root.
2.  Update the variables at the top:
    - `PROJECT_ID`: Your GCP project ID.
    - `MONGO_URI`: Your MongoDB Atlas connection string.
    - `GEMINI_API_KEY`: Your Google Gemini API Key.
    - `NEXTAUTH_SECRET`: Any random string for security.
3.  Run the script:
    ```bash
    chmod +x deploy.sh
    ./deploy.sh
    ```

## 4. Post-Deployment
- The script will output the **Frontend URL**.
- You may need to add the Frontend URL to the `NEXTAUTH_URL` environment variable in the Google Cloud Console (Cloud Run -> medtech-frontend -> Edit & Deploy New Revision).

## 💡 Cost Saving Tip
Cloud Run only charges you when the services are being used. Since this is for a presentation, it will likely cost you $0 from your free credits!
