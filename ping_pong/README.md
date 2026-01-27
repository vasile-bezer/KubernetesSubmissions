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