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