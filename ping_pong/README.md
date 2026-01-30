## Ping pong app

- docker build -t ping_pong ./ping_pong/ && k3d image import ping_pong:latest
- kubectl apply -f ping_pong/manifests/deployment.yaml
- kubectl apply -f ping_pong/manifests/ingress.yaml
- kubectl apply -f ping_pong/manifests/service.yaml

## Debug 

- kubectl get pods -l app=ping-pong -o wide
- kubectl get svc ping-pong-svc
- kubectl get ingress ping-pong-ingress -o yaml
- kubectl delete ingress ping-pong-ingress && sleep 2 && kubectl apply -f ping_pong/manifests/ingress.yaml
- kubectl rollout restart deployment/ping-pong-dep && kubectl rollout status deployment/ping-pong-dep

# Persistency

- cd ping_pong && docker build -t ping_pong:latest .
- kubectl apply -f manifests/deployment.yaml
- kubectl rollout restart deployment/ping-pong-dep
- kubectl rollout status deployment/ping-pong-dep

To debug

- kubectl get pods -l app=ping-pong
- kubectl exec $(kubectl get pod -l app=ping-pong -o jsonpath='{.items[0].metadata.name}') -- ls -la /app/data/ 2>&1
- kubectl exec ping-pong-dep-7bf6969f88-h7q8n -- cat /app/data/pingpong_counter.txt 2>&1
- kubectl logs ping-pong-dep-7bf6969f88-h7q8n --tail=20
- kubectl exec ping-pong-dep-7bf6969f88-h7q8n -- python3 -c "import os; print('Can write:', os.access('/app/data', os.W_OK)); print('Dir exists:', os.path.exists('/app/data'))"

## Connecting pods

- cd ping_pong && docker build -f Dockerfile -t ping_pong:latest . && k3d image import ping_pong:latest
- kubectl apply -f manifests/deployment.yaml
- kubectl rollout restart deployment/ping-pong-dep
- kubectl rollout status deployment/ping-pong-dep

## GKE

- gcloud config set project dwk-gke-485823
- gcloud container clusters create dwk-cluster --zone=europe-north1-b --cluster-version=1.32 --disk-size=32 --num-nodes=3 --machine-type=e2-micro
- sudo apt-get install google-cloud-cli-gke-gcloud-auth-plugin
- cloud container clusters get-credentials dwk-cluster --zone europe-north1-b --project dwk-gke-485823
- kubectl get nodes
- kubectl cluster-info
- kubectl create namespace exercises
- cd ping_pong && docker build -t gcr.io/dwk-gke-485823/ping-pong:latest .
- gcloud auth configure-docker
- kubectl apply -f ping_pong/manifests-gke
- curl http://35.228.175.222/pingpong