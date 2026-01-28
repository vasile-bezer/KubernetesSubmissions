# Busybox

- kubectl apply -f busybox/manifests/deployment.yaml
- kubectl exec -it my-busybox -- wget -qO - http://localhost:8081/
- kubectl exec -it my-busybox -- wget -qO - http://localhost:8081/pingpong

- kubectl exec -it my-busybox -- sh

To delete pod

- kubectl delete pod/my-busybox