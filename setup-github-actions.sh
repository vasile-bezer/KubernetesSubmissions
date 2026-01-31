#!/bin/bash

# Setup script for GitHub Actions deployment to GKE

# Variables
PROJECT_ID="dwk-gke-485823"
SERVICE_ACCOUNT_NAME="github-actions"
SERVICE_ACCOUNT_EMAIL="${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"

echo "Setting up GitHub Actions service account for GKE deployment..."

# Create service account
echo "Creating service account..."
gcloud iam service-accounts create ${SERVICE_ACCOUNT_NAME} \
  --display-name="GitHub Actions" \
  --project=${PROJECT_ID}

# Grant necessary roles
echo "Granting roles..."
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member="serviceAccount:${SERVICE_ACCOUNT_EMAIL}" \
  --role="roles/container.developer"

gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member="serviceAccount:${SERVICE_ACCOUNT_EMAIL}" \
  --role="roles/artifactregistry.writer"

gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member="serviceAccount:${SERVICE_ACCOUNT_EMAIL}" \
  --role="roles/storage.admin"

# Create and download key
echo "Creating service account key..."
gcloud iam service-accounts keys create ./github-actions-key.json \
  --iam-account=${SERVICE_ACCOUNT_EMAIL}

echo ""
echo "✅ Service account created successfully!"
echo ""
echo "Next steps:"
echo "1. Go to your GitHub repository: https://github.com/vasile-bezer/KubernetesSubmissions/settings/secrets/actions"
echo "2. Create a new secret named 'GKE_SA_KEY'"
echo "3. Copy the contents of github-actions-key.json and paste it as the secret value"
echo "4. Create another secret named 'GKE_PROJECT' with value: ${PROJECT_ID}"
echo ""
echo "To get the key content, run:"
echo "cat github-actions-key.json"
echo ""
echo "⚠️  IMPORTANT: Delete github-actions-key.json after setting up the secret!"
