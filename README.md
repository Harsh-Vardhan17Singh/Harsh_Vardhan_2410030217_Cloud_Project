# Cloud Computing Project: Visitor Counter on Docker & Kubernetes with Hybrid Failover

**Author:** Harsh Vardhan  
**Student ID / Roll No:** 2410030217  
**GitHub Repository:** https://github.com/Harsh-Vardhan17Singh/Harsh_Vardhan_2410030217_Cloud_Project  

A complete, production-grade implementation of a containerized Visitor Counter Web Application (Python Flask + Redis) deployed to Kubernetes with Horizontal Pod Autoscaler (HPA v2), simulated Hybrid Cloud disaster recovery failover, and comprehensive FinOps cost optimization analysis.

---

## Project Structure

```text
├── app.py                            # Flask web application with /healthz, /readyz, /load
├── requirements.txt                  # Python dependencies (Flask, Redis, Gunicorn)
├── Dockerfile                        # Multi-stage optimized production Dockerfile (142 MB)
├── Dockerfile.unoptimized            # Baseline unoptimized Dockerfile for cost analysis
├── docker-compose.yml                # Docker Compose orchestration (Web + Redis)
├── k8s.yaml                          # Complete Kubernetes manifests (ConfigMap, PVC, Redis, Web)
├── hpa.yaml                          # HorizontalPodAutoscaler (CPU 50%, Memory 75%)
├── github_link.txt                   # Public GitHub repository reference
├── PROJECT_REPORT.md                 # Formal project report for submission
├── templates/
│   └── index.html                    # Modern web interface with real-time stats & load generator
├── hybrid_cloud/
│   ├── cluster-primary.yaml          # Primary cluster (Simulated On-Premises) manifests
│   ├── cluster-secondary.yaml        # Secondary cluster (Simulated Public Cloud) manifests
│   ├── nginx-failover.conf           # Nginx upstream backup configuration
│   ├── failover_router.py            # Global Traffic Manager & health-checking reverse proxy
│   ├── simulate_hybrid_failover.ps1  # Automated failover test script (PowerShell)
│   └── simulate_hybrid_failover.sh   # Automated failover test script (Bash)
├── cost_optimization/
│   └── cost_analysis_report.md       # Detailed FinOps report with 3 measured techniques
├── scripts/
│   └── load_test.py                  # Concurrent load generator script for HPA testing
├── architecture/
│   └── architecture_diagram.svg      # High-resolution architectural diagram
└── screenshots/
    └── README.md                     # Instructions and commands for all required screenshots
```

---

## Quickstart Guide

### 1. Run with Docker Compose
```bash
docker compose up -d
docker compose ps
```
Access the application at `http://localhost:5000`.

### 2. Deploy to Kubernetes
```bash
# Build and load image into your Kubernetes environment (e.g., Minikube)
minikube image build -t visitor-counter:latest .
# or: docker build -t visitor-counter:latest . && minikube image load visitor-counter:latest

# Apply Kubernetes manifests
kubectl apply -f k8s.yaml

# Verify resources
kubectl get all -l app=visitor-counter
kubectl get pvc
```
Access the application on NodePort:
```bash
minikube service visitor-counter-service
# Or directly at http://<minikube-ip>:30005
```

### 3. Deploy and Test HPA Autoscaling
```bash
# Ensure metrics-server is active
minikube addons enable metrics-server

# Deploy HPA
kubectl apply -f hpa.yaml
kubectl get hpa visitor-counter-hpa

# Run load generator
python scripts/load_test.py http://localhost:5000/load?duration=3 15 90

# Watch pods autoscale
kubectl get pods -l app=visitor-counter -w
```

### 4. Run Hybrid Cloud Failover Simulation
Open two terminals:

**Terminal 1 (Start Global Traffic Manager / Failover Router):**
```bash
python hybrid_cloud/failover_router.py
```

**Terminal 2 (Run Failover Simulation):**
```powershell
powershell -ExecutionPolicy Bypass -File hybrid_cloud/simulate_hybrid_failover.ps1
```
Or manually trigger failover:
```bash
# Simulate primary failure
kubectl scale deployment visitor-counter-web --replicas=0
# Observe traffic routing instantly to secondary cluster

# Restore primary
kubectl scale deployment visitor-counter-web --replicas=2
# Observe automatic failback
```

---

## Required Submission Instructions
1. Push this entire project to a **PUBLIC** GitHub repository.
2. Update `github_link.txt` with your public GitHub repository URL.
3. Download the repository as a ZIP file: GitHub &rarr; Code &rarr; Download ZIP.
4. Upload to the Google Drive link specified by the instructor:
   - Complete ZIP file.
   - Your Team Research Paper (previously assigned).
   - All captured screenshots in the `screenshots/` directory.

