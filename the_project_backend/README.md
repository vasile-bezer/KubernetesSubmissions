## Todo app backend

- cd the_project_backend && docker build -t the_project_backend:latest . && k3d image import the_project_backend:latest
- kubectl rollout restart deployment/todo-backend-dep
- kubectl apply -f ./manifests/

To debug

- kubectl rollout restart deployment/todo-backend-dep