## Log output app

To run: python3 log_output or python3 __main__.py
To run with kubernetes: 
- docker build . -t log_output then 
- k3d image import log_output:latest then
- kubectl create deployment log-output-dep --image=log_output:latest then
- kubectl edit deployment log-output-dep (set PullPolicy to Never) then
- kubectl logs -f log-output-dep-58b8759476-rckqz
To run with manifests:
- kubectl apply -f manifests/deployment.yaml
- kubectl logs -f deployment/log-output-dep

## Ingress

(do this after doing Node port in 1.6)

- docker rmi log_output
- docker build -t log_output ./log_output/
- k3d image import log_output:latest
- kubectl apply -f log_output/manifests/deployment.yaml
- kubectl apply -f log_output/manifests/ingress.yaml
- kubectl apply -f log_output/manifests/service.yaml

To debug
- kubectl get ingress log-output-ingress -o yaml
- kubectl get svc log-output-svc
- kubectl get ingress
- kubectl logs -l app=log-output --tail=20

## Storage

- cd log_output && docker build -f Dockerfile.writer -t log_output_writer:latest . && docker build -f Dockerfile.reader -t log_output_reader:latest .
- k3d image import log_output_writer:latest log_output_reader:latest
- kubectl apply -f log_output/manifests/deployment.yaml
- kubectl rollout status deployment/log-output-dep


To debug
- kubectl logs -l app=log-output -c log-writer --tail=5
- kubectl logs -l app=log-output -c log-reader --tail=5
- kubectl get pods -l app=log-output --field-selector=status.phase=Running -o name | head -1 | xargs kubectl logs -c log-writer --tail=5
- kubectl get pods -l app=log-output --field-selector=status.phase=Running -o name | head -1 | xargs kubectl logs -c log-reader --tail=5
- kubectl get ingress
- kubectl port-forward $(kubectl get pod -l app=log-output --field-selector=status.phase=Running -o name | head -1) 9999:3000 &
- kubectl describe pod $(kubectl get pod -l app=log-output --field-selector=status.phase=Running -o jsonpath='{.items[0].metadata.name}') | grep -A 10 "log-reader"
- kubectl exec $(kubectl get pod -l app=log-output --field-selector=status.phase=Running -o jsonpath='{.items[0].metadata.name}') -c log-reader -- sh -c 'echo "LOG_FILE=$LOG_FILE PORT=$PORT" && ls -la /app/logs/ && cat /app/logs/output.txt 2>&1 || echo "File not found"'
- kubectl get deployment log-output-dep -o yaml | grep -A 50 "spec:" | head -60

## Persistency

- cd log_output && docker build -f Dockerfile.writer -t log_output_writer:latest . && docker build -f Dockerfile.reader -t log_output_reader:latest .
- kubectl apply -f manifests/deployment.yaml
- kubectl rollout restart deployment/log-output-dep
- kubectl rollout status deployment/log-output-dep

To debug

- kubectl exec $(kubectl get pod -l app=log-output --field-selector=status.phase=Running -o jsonpath='{.items[0].metadata.name}') -c log-reader -- sh -c 'ls -la /app/data/ && cat /app/data/pingpong_counter.txt 2>&1'
- kubectl get pods -l app=log-output
- kubectl exec log-output-dep-5f7b86d9c-qfd82 -c log-reader -- ls -la /app/data/ 2>&1

## Connecting pods

- cd log_output && docker build -f Dockerfile.reader -t log_output_reader:latest . && k3d image import log_output_reader:latest
- k3d image import log_output_writer:latest
- kubectl apply -f manifests/deployment.yaml
- kubectl rollout restart deployment/log-output-dep
- kubectl rollout status deployment/log-output-dep

To debug

- kubectl delete pod log-output-dep-76cd79b84-sj4ct
- kubectl edit deployment log-output-dep
- kubectl delete -f manifests/deployment.yaml
- docker exec k3d-k3s-default-agent-0 crictl images

## Namespaces

- kubectl create namespace exercises

To debug

- kubectl get pods -n kube-system
- kubectl get all --all-namespaces
- kubectl config set-context --current --namespace=<name>
- kubectl get all -n exercises
- kubectl delete deployment log-output-dep ping-pong-dep -n exercises
- kubectl delete service,ingress --all -n exercises
- kubectl get all,ingress -n exercises
- kubectl rollout restart deployment/log-output-dep -n exercises
- kubectl get pods -n exercises

To create a new namespace for the app

- kubectl delete deployment log-output-dep ping-pong-dep -n log-output-namespace
- kubectl delete service,ingress --all -n log-output-namespace
- 

## Gateway API

- $ gcloud container clusters update dwk-cluster --location=europe-north1-b --gateway-api=standard
- kubectl delete -f log_output/manifests-gke/ingress.yaml
- kubectl apply -f log_output/manifests-gke/gateway.yaml
- kubectl apply -f log_output/manifests-gke/route.yaml


To debug

- kubectl get gatewayclass
- kubectl describe gateway my-gateway -n exercises

## Rewritten routing

- cd ping_pong && docker build -t europe-north1-docker.pkg.dev/dwk-gke-485823/ping-pong/ping-pong:latest .
- docker push europe-north1-docker.pkg.dev/dwk-gke-485823/ping-pong/ping-pong:latest
- kubectl apply -f /home/percy/Scrivania/KubernetesSubmissions/log_output/manifests-gke/route.yaml
- kubectl rollout restart deployment ping-pong-dep -n exercises