#!/bin/bash

# Setup Workload Identity Federation for GitHub Actions

PROJECT_ID="dwk-gke-485823"
PROJECT_NUMBER=$(gcloud projects describe ${PROJECT_ID} --format="value(projectNumber)")
SERVICE_ACCOUNT="github-actions@${PROJECT_ID}.iam.gserviceaccount.com"
WORKLOAD_IDENTITY_POOL="github-actions-pool"
WORKLOAD_IDENTITY_PROVIDER="github-actions-provider"
REPO="vasile-bezer/KubernetesSubmissions"

echo "Setting up Workload Identity Federation for GitHub Actions..."
echo "Project ID: ${PROJECT_ID}"
echo "Project Number: ${PROJECT_NUMBER}"
echo "Repository: ${REPO}"
echo ""

# Enable required APIs
echo "Enabling required APIs..."
gcloud services enable iamcredentials.googleapis.com --project=${PROJECT_ID}
gcloud services enable sts.googleapis.com --project=${PROJECT_ID}

# Create Workload Identity Pool
echo "Creating Workload Identity Pool..."
gcloud iam workload-identity-pools create "${WORKLOAD_IDENTITY_POOL}" \
  --project="${PROJECT_ID}" \
  --location="global" \
  --display-name="GitHub Actions Pool" \
  2>/dev/null || echo "Pool already exists"

# Create Workload Identity Provider
echo "Creating Workload Identity Provider..."
gcloud iam workload-identity-pools providers create-oidc "${WORKLOAD_IDENTITY_PROVIDER}" \
  --project="${PROJECT_ID}" \
  --location="global" \
  --workload-identity-pool="${WORKLOAD_IDENTITY_POOL}" \
  --display-name="GitHub Actions Provider" \
  --attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.repository=assertion.repository" \
  --issuer-uri="https://token.actions.githubusercontent.com" \
  2>/dev/null || echo "Provider already exists"

# Allow the Workload Identity to impersonate the service account
echo "Setting up IAM policy binding..."
gcloud iam service-accounts add-iam-policy-binding "${SERVICE_ACCOUNT}" \
  --project="${PROJECT_ID}" \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/${WORKLOAD_IDENTITY_POOL}/attribute.repository/${REPO}"

# Get the Workload Identity Provider resource name
WIF_PROVIDER="projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/${WORKLOAD_IDENTITY_POOL}/providers/${WORKLOAD_IDENTITY_PROVIDER}"

echo ""
echo "✅ Workload Identity Federation setup complete!"
echo ""
echo "Next steps:"
echo "1. Go to your GitHub repository: https://github.com/${REPO}/settings/secrets/actions"
echo "2. Create a new secret named 'WIF_PROVIDER' with the following value:"
echo ""
echo "${WIF_PROVIDER}"
echo ""
echo "Then commit and push your .github/workflows/main.yaml file to trigger the workflow!"
