## Log output app

To run: python3 the_project or python3 __main__.py
To run with kubernetes: 
- docker build . -t the_project then 
- k3d image import the_project:latest then
- kubectl create deployment the-project-dep --image=the_project:latest then
- kubectl edit deployment the-project-dep (set PullPolicy to Never) then
- kubectl logs -f the-project-dep-6995b7bb9f-xdbnd
- kubectl port-forward the-project-dep-6995b7bb9f-xdbnd 3000:3000
- curl http://localhost:3000/ -> ok

## Node port

- k3d cluster delete
- k3d cluster create --port 8082:30080@agent:0 -p 8081:80@loadbalancer --agents 2
- k3d image import the_project:latest
- kubectl apply -f the_project/manifests/service.yaml
- kubectl apply -f the_project/manifests/service.yaml
- curl http://localhost:8082/ -> ok

# Ingress

(do this after Ingress in 1.7)

- kubectl delete ingress log-output-ingress
- kubectl apply -f the_project/manifests/service.yaml
- kubectl apply -f the_project/manifests/service.yaml

# Remove boredom

- cd the_project && docker build -t the_project:latest . && k3d image import the_project:latest
- kubectl apply -f the_project/manifests/deployment.yaml
- kubectl rollout status deployment/the-project-dep
- kubectl delete ingress log-output-ingress
- kubectl apply -f the_project/manifests/ingress.yaml

# Add todo list

- cd the_project && docker build -t the_project:latest . && k3d image import the_project:latest
- kubectl rollout restart deployment/the-project-dep

## Todo app backend

- cd the_project && docker build -t the_project:latest . && k3d image import the_project:latest
- kubectl rollout restart deployment/the-project-dep
- kubectl apply -f ./manifests/ingress.yaml

To debug

- kubectl describe ingress


## Namespaces

- kubectl create namespace project

To debug

- kubectl get pods -n kube-system
- kubectl get all --all-namespaces
- kubectl config set-context --current --namespace=<name>
- kubectl get all -n project
- kubectl delete deployment log-output-dep ping-pong-dep -n project
- kubectl delete service,ingress --all -n project
- kubectl get all,ingress -n project
- kubectl rollout restart deployment/log-output-dep -n project
- kubectl get pods -n project

## Kustomize

Build and push images:
- cd the_project && docker build -t europe-north1-docker.pkg.dev/dwk-gke-485823/the-project/the-project:latest . && docker push europe-north1-docker.pkg.dev/dwk-gke-485823/the-project/the-project:latest
- cd the_project_backend && docker build -t europe-north1-docker.pkg.dev/dwk-gke-485823/the-project/the-project-backend:latest . && docker push europe-north1-docker.pkg.dev/dwk-gke-485823/the-project/the-project-backend:latest

Deploy to GKE with Kustomize:
- kubectl apply -k .
- kubectl get gateway -n project
- kubectl get httproute -n project
- kubectl get pods -n project

Access the app:
- Get Gateway IP: kubectl get gateway the-project-gateway -n project -o jsonpath='{.status.addresses[0].value}'
- Frontend: http://34.111.231.229/
- Backend API: http://34.111.231.229/todos

To update:
- kubectl rollout restart deployment/the-project-dep -n project
- kubectl rollout restart deployment/todo-backend-dep -n project

To debug:
- kubectl describe gateway the-project-gateway -n project
- kubectl describe httproute the-project-route -n project
- kubectl logs -n project deployment/todo-backend-dep
- gcloud compute backend-services get-health <backend-service-name> --global

## Automatic deployment

Setup scripts (easier):
- bash setup-github-actions.sh
- bash setup-workload-identity.sh

Or manual setup:
- gcloud iam service-accounts create github-actions --display-name="GitHub Actions" --project=dwk-gke-485823
- gcloud projects add-iam-policy-binding dwk-gke-485823 --member="serviceAccount:<service-account-email>" --role="roles/container.developer"
- gcloud projects add-iam-policy-binding dwk-gke-485823 --member="serviceAccount:<service-account-email>" --role="roles/artifactregistry.writer"
- gcloud projects add-iam-policy-binding dwk-gke-485823 --member="serviceAccount:<service-account-email>" --role="roles/storage.admin"
- gcloud iam workload-identity-pools create github-actions-pool --location=global --display-name="GitHub Actions Pool" --project=dwk-gke-485823
- gcloud iam workload-identity-pools providers create-oidc github-actions-provider --workload-identity-pool=github-actions-pool --location=global --issuer-uri="https://token.actions.githubusercontent.com" --attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.repository=assertion.repository,attribute.repository_owner=assertion.repository_owner" --attribute-condition="assertion.repository_owner=='<repo-owner>'" --project=dwk-gke-485823
- gcloud iam service-accounts add-iam-policy-binding <service-account-email> --project=dwk-gke-485823 --role="roles/iam.workloadIdentityUser" --member="principalSet://iam.googleapis.com/projects/<GCP Project Number>/locations/global/workloadIdentityPools/github-actions-pool/attribute.repository/<repo-owner>/KubernetesSubmissions"

GitHub Secrets (in "the_project" environment):
- WIF_PROVIDER: gcloud iam workload-identity-pools providers describe github-actions-provider --workload-identity-pool=github-actions-pool --location=global --project=<PROJECT_ID> --format="value(name)"
- GKE_PROJECT: gcloud config get-value project
- GKE_SA_EMAIL: gcloud iam service-accounts list --filter="displayName:GitHub Actions" --format="value(email)"

## Each branch creates a separate environment

- Push to any branch triggers automatic deployment
- main branch deploys to namespace: project
- Other branches deploy to namespace: <branch-name>
- Each branch gets its own isolated environment with separate Gateway
- Images are built with commit SHA tags
- Kustomize automatically updates namespace and images using: kustomize edit set namespace ${GITHUB_REF#refs/heads/}
- Example: feature-branch deploys to namespace "feature-branch"
- Branch names must be valid Kubernetes namespace names

Automatic cleanup:
- Deleting a branch triggers automatic cleanup workflow
- Deletes the namespace and all resources (Gateway, deployments, services, etc.)
- main branch namespace (project) is protected from deletion
- Workflow: .github/workflows/cleanup.yaml



# Test branch deployment
