# Wikipedia Todo CronJob

This CronJob generates a new todo every hour with a random Wikipedia article URL.

## How it works

The CronJob uses the Wikipedia Special:Random endpoint which redirects to a random article. The script:
1. Fetches https://en.wikipedia.org/wiki/Special:Random
2. Follows the redirect to get the actual article URL
3. Creates a todo with text "Read <URL>"
4. POSTs the todo to the backend service

## Build and Deploy

```bash
# Build the Docker image
docker build -t wikipedia-cron:latest wikipedia_cron/

# Import to k3d cluster
k3d image import wikipedia-cron:latest -c k3s-default

# Deploy the CronJob
kubectl apply -f wikipedia_cron/manifests/cronjob.yaml

# Check CronJob status
kubectl get cronjobs -n project

# Manually trigger a job for testing
kubectl create job --from=cronjob/wikipedia-todo-cron wikipedia-test -n project

# Check job logs
kubectl logs -n project -l job-name=wikipedia-test
```

## Configuration

The CronJob runs every hour (schedule: "0 * * * *"). You can modify the schedule in the cronjob.yaml file using standard cron syntax.

The backend service URL uses the correct port (2345) which is the ClusterIP service port that forwards to the backend container's port 3001.

## Environment Variables

- `BACKEND_URL`: URL of the todo backend service (default: http://todo-backend-svc.project.svc.cluster.local:2345/todos)
