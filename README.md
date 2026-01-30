## TO RUN FOLLOW THE STEPS BELOW

# 1. Prerequisites

A running Kubernetes cluster and kubectl configured to point at the cluster

# 2. To deploy

cd frtn90-project/scripts
kubectl apply -f 00-namespace.yaml
kubectl apply -f 01-app-config.yaml
kubectl apply -f 02-app-secrets.yaml
kubectl apply -f 10-redis.yaml
kubectl apply -f 20-rabbitmq.yaml
kubectl apply -f 30-app-deployment.yaml
kubectl apply -f 31-app-hpa.yaml
kubectl apply -f 40-worker-deployment.yaml
kubectl apply -f 41-worker-hpa.yaml
kubectl apply -f 50-nginx-deployment.yaml

# Data service (encapsulates Redis)

kubectl apply -f 60-data-deployment.yaml
kubectl apply -f 61-data-service.yaml

# Note: Redis is encapsulated in 'data-service'. App/Worker communicate only with the data-service HTTP API.

**Troubleshooting:** If `kubectl apply` fails with an error like "failed to download openapi... connectex: connection refused" your `kubectl` cannot reach the Kubernetes API server (client-side validation fetches the OpenAPI schema).

- Quick workaround: run `kubectl apply -f 60-data-deployment.yaml --validate=false` (or add `--validate=false` to the above commands).
- Check connectivity and context:
  - `kubectl cluster-info`
  - `kubectl config current-context`
  - `kubectl get nodes`
  - `kubectl version --short`
- Ensure your kubeconfig/context points to a reachable API server and that no environment variables (eg. `KUBERNETES_MASTER`) are forcing localhost:8080.

# 3. To check the status of all of the pods

kubectl get pods -n post-it

# 4. To access the app

kubectl -n post-it port-forward svc/nginx-frontend 8080:80
kubectl -n post-it port-forward svc/app 5000:5000
kubectl -n post-it patch svc/nginx-frontend -p '{"spec": {"type": "NodePort", "ports": [{"port": 80, "targetPort": 80, "nodePort": 30080}]}}'

# 5. To demonstrate autoscaling

kubectl get hpa -n post-it --watch
#in a different terminal
python workload-generator/dynamic-workload-generator.py
#in a different terminal
#then return to the first terminal to watch the pods scale
curl -X POST http://localhost:5000/workload  
 -H "Content-Type: application/json"  
 -d '{"url": "<your-port-and-endpoint>/api/post", "rate": 50}'

# 6. To demonstrate resilience

kubeclt get pods -n post-it
kubectl delete pod <pod-name> -n post-it
kubeclt get pods -n post-it

# 7. To demonstrate rolling-update with CI/CD
