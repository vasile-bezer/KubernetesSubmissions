# Automatic Deployment Setup

This project uses GitHub Actions with Google Cloud Workload Identity Federation for automatic deployment to GKE.

## Setup Complete ✅

The following has been configured:

1. **Service Account**: `github-actions@dwk-gke-485823.iam.gserviceaccount.com`
   - Roles: Container Developer, Artifact Registry Writer, Storage Admin

2. **Workload Identity Federation**: Configured for secure keyless authentication

3. **GitHub Workflow**: `.github/workflows/main.yaml`
   - Triggers on push to `main` branch
   - Builds and pushes Docker images for frontend and backend
   - Deploys to GKE using Kustomize
   - Restarts deployments to use new images

4. **Deployment Strategy**: Changed to `Recreate` for ReadWriteOnce PVC compatibility

## Required GitHub Secrets

You need to add THREE secrets to the GitHub **environment** called "the_project":

1. Go to: https://github.com/vasile-bezer/KubernetesSubmissions/settings/environments

2. Click on the "the_project" environment (or create it if it doesn't exist)

3. Click "Add environment secret" for each of the following:

### Secret 1: WIF_PROVIDER
   
   Value:
   ```
   projects/715298517821/locations/global/workloadIdentityPools/github-actions-pool/providers/github-actions-provider
   ```

### Secret 2: GKE_PROJECT
   
   Value:
   ```
   dwk-gke-485823
   ```

### Secret 3: GKE_SA_EMAIL
   
   Value:
   ```
   github-actions@dwk-gke-485823.iam.gserviceaccount.com
   ```

## How It Works

1. You push code to the `main` branch
2. GitHub Actions workflow automatically:
   - Builds frontend image: `europe-north1-docker.pkg.dev/dwk-gke-485823/the-project/the-project-frontend`
   - Builds backend image: `europe-north1-docker.pkg.dev/dwk-gke-485823/the-project/the-project-backend`
   - Pushes images with both `latest` and commit SHA tags
   - Applies Kustomize configuration to GKE
   - Restarts deployments to use new images
   - Waits for rollout to complete

3. Your application is automatically deployed to: http://34.111.231.229/

## Deployment Strategy

The frontend deployment uses `Recreate` strategy because it uses a `ReadWriteOnce` PVC. This means:
- The old pod is terminated before the new pod is created
- No downtime risk from PVC mount conflicts
- Brief downtime during updates (typically < 30 seconds)

## Testing the Workflow

To test the automatic deployment:

```bash
# Make a change to the code
echo "# Test change" >> the_project/README.md

# Commit and push
git add .
git commit -m "Test automatic deployment"
git push

# Watch the workflow
# Visit: https://github.com/vasile-bezer/KubernetesSubmissions/actions
```

## Manual Deployment (if needed)

If you need to deploy manually:

```bash
# Build and push images
cd the_project && docker build -t europe-north1-docker.pkg.dev/dwk-gke-485823/the-project/the-project-frontend:latest . && docker push europe-north1-docker.pkg.dev/dwk-gke-485823/the-project/the-project-frontend:latest

cd ../the_project_backend && docker build -t europe-north1-docker.pkg.dev/dwk-gke-485823/the-project/the-project-backend:latest . && docker push europe-north1-docker.pkg.dev/dwk-gke-485823/the-project/the-project-backend:latest

# Deploy
cd ..
kubectl apply -k .
kubectl rollout restart deployment/the-project-dep -n project
kubectl rollout restart deployment/todo-backend-dep -n project
```

## Troubleshooting

If the workflow fails:

1. Check the GitHub Actions logs: https://github.com/vasile-bezer/KubernetesSubmissions/actions

2. Verify the WIF_PROVIDER secret is set correctly

3. Check GKE cluster status:
   ```bash
   kubectl get pods -n project
   kubectl describe deployment/the-project-dep -n project
   kubectl describe deployment/todo-backend-dep -n project
   ```

4. Check Gateway status:
   ```bash
   kubectl get gateway -n project
   kubectl describe gateway the-project-gateway -n project
   ```
