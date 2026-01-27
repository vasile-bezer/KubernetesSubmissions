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
