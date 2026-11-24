# Mandatory Project Screenshots Guide

According to the project instructions, you must capture and submit clear screenshots demonstrating each required phase. Use this guide to capture all 6 required screenshots.

---

### Screenshot 1: Containerized Application Running in Docker
- **Goal:** Demonstrate that the Flask app and Redis container are up and running via Docker / Docker Compose.
- **Commands to run:**
  ```powershell
  docker compose up -d
  docker compose ps
  curl http://localhost:5000
  ```
- **What to capture:**
  - The terminal showing `docker compose ps` with both `visitor-counter-app` and `visitor-counter-redis` with `Up` status and ports `5000->5000` and `6379->6379`.
  - Browser showing `http://localhost:5000` with the Visitor Counter UI incrementing.

---

### Screenshot 2: Kubernetes Deployment & Running Pods
- **Goal:** Demonstrate successful deployment of Deployments, Services, and Persistent Volumes in Kubernetes.
- **Commands to run:**
  ```powershell
  kubectl apply -f k8s.yaml
  kubectl get all -l app=visitor-counter
  kubectl get pvc
  ```
- **What to capture:**
  - Terminal displaying:
    - Pods: `visitor-counter-web-xxxx` (2/2 Running), `redis-deployment-xxxx` (1/1 Running)
    - Services: `redis-service` (ClusterIP), `visitor-counter-service` (NodePort)
    - PVC: `redis-pvc` status `Bound`

---

### Screenshot 3: Kubernetes Self-Healing (Pod Recovery)
- **Goal:** Demonstrate Kubernetes automated self-healing by deleting a running pod and observing the ReplicaSet automatically launching a replacement pod.
- **Commands to run:**
  ```powershell
  # Check pods
  kubectl get pods -l app=visitor-counter
  # Delete one web pod
  kubectl delete pod <web-pod-name>
  # Immediately inspect pods
  kubectl get pods -l app=visitor-counter
  ```
- **What to capture:**
  - Terminal showing the old pod in `Terminating` state and a brand new replacement pod in `ContainerCreating` or `Running` within seconds, maintaining replica count = 2.

---

### Screenshot 4: Horizontal Pod Autoscaler (HPA) Scaling Under Load
- **Goal:** Demonstrate dynamic pod autoscaling when CPU utilization exceeds 50%.
- **Commands to run:**
  ```powershell
  # Enable metrics-server if using Minikube:
  minikube addons enable metrics-server

  # Apply HPA:
  kubectl apply -f hpa.yaml

  # Check initial HPA state (replicas = 2):
  kubectl get hpa visitor-counter-hpa

  # Run load test generator in a separate window:
  python scripts/load_test.py http://<minikube-ip>:30005/load?duration=3 15 90

  # Observe scaling:
  kubectl get hpa visitor-counter-hpa -w
  kubectl get pods -l app=visitor-counter
  ```
- **What to capture:**
  - Terminal displaying HPA TARGETS rising (e.g. `120%/50%`) and REPLICAS scaling out from `2` to `4` or more.
  - Pod listing showing new scaled replicas in `Running` state.

---

### Screenshot 5: Hybrid Cloud Steady State (Traffic Routing to Primary)
- **Goal:** Demonstrate health-monitored routing to the Primary Cluster (simulated On-Premises).
- **Commands to run:**
  ```powershell
  python hybrid_cloud/failover_router.py
  # In another terminal:
  curl http://localhost:8080/healthz
  ```
- **What to capture:**
  - Terminal showing router log: `[PRIMARY] GET /healthz -> Status 200` and response JSON with `"cluster": "Primary-Cluster (On-Premises Data Center)"`.
  - Browser accessing `http://localhost:8080` showing the Primary Cluster badge.

---

### Screenshot 6: Hybrid Cloud Automated Failover to Secondary (Cloud)
- **Goal:** Demonstrate automatic traffic failover to Secondary Cluster when Primary cluster fails.
- **Commands to run:**
  ```powershell
  # In terminal 2, simulate Primary outage:
  kubectl scale deployment visitor-counter-web --replicas=0

  # Observe router terminal:
  # Shows: [FAILOVER EVENT] Primary Cluster UNREACHABLE! --> AUTOMATIC FAILOVER to Secondary

  # Send requests:
  curl http://localhost:8080/healthz
  ```
- **What to capture:**
  - Terminal showing the router detecting the outage and routing traffic to `SECONDARY (Public Cloud Failover)`.
  - Browser showing `http://localhost:8080` displaying the Secondary Cluster badge without error (HTTP 200).

