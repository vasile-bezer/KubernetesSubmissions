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
