## Todo app backend

- cd the_project_backend && docker build -t the_project_backend:latest . && k3d image import the_project_backend:latest
- kubectl rollout restart deployment/todo-backend-dep
- kubectl apply -f ./manifests/

To debug

- kubectl rollout restart deployment/todo-backend-dep

# Logging

- curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-4
- chmod 700 get_helm.sh
- ./get_helm.sh
- helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
- helm repo add stable https://charts.helm.sh/stable
- helm repo update
- kubectl create namespace prometheus
- helm install prometheus-community/kube-prometheus-stack --generate-name --namespace prometheus
- kubectl get po -n prometheus
- kubectl -n prometheus port-forward kube-prometheus-stack-1602180058-grafana-59cd48d794-4459m 3000
- helm repo add grafana https://grafana.github.io/helm-charts
- helm repo update
- kubectl create namespace loki-stack
- helm upgrade --install loki --namespace=loki-stack grafana/loki-stack --set loki.image.tag=2.9.3
- kubectl get all -n loki-stack
- 


To debug

- kubectl get secret -n prometheus
- kubectl get secret kube-prometheus-stack-1769709743-grafana -n prometheus -o jsonpath="{.data.admin-password}" | base64 --decode && echo
