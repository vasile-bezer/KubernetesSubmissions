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