## Log output app

To run: python3 the_project or python3 __main__.py
To run with kubernetes: 
- docker build . -t the_project then 
- k3d image import the_project:latest then
- kubectl create deployment the-project-dep --image=the_project:latest then
- kubectl edit deployment the-project-dep (set PullPolicy to Never) then
- kubectl logs -f the-project-dep-8668564684-p9zlf
To run with manifests:
- kubectl delete deployment the-project-dep
- k3d image import the_project:latest -c k3s-default
- kubectl apply -f manifests/deployment.yaml
- kubectl logs -f deployment/the-project-dep