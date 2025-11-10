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