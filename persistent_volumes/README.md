# Deploy persistent volume

(do this after creating the cluster)

- docker exec k3d-k3s-default-agent-0 mkdir -p /tmp/kube
- kubectl apply -f persistent_volumes/manifests/persistentvolume.yaml
- kubectl apply -f persistent_volumes/manifests/persistentvolumeclaim.yaml

To debug

- kubectl delete pvc shared-pvc
- kubectl get pv,pvc