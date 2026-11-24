# Project Execution Screenshots Catalog

**Student Name:** Harsh Vardhan  
**Student ID / Roll No:** 2410030217  
**Repository:** https://github.com/Harsh-Vardhan17Singh/Harsh_Vardhan_2410030217_Cloud_Project  

This directory contains all 15 captured verification screenshots covering every required task of the Cloud Computing Project.

---

## Index of Screenshots

| # | Filename | Task Covered | Description |
|---|:---|:---|:---|
| 01 | `01_environment_versions.png` | Environment Setup | Verification of Docker 29.5, Compose v5.1, Minikube v1.39, Kubectl v1.37, Python 3.14 |
| 02 | `02_docker_build.jpg` | Task 1: Containerization | Docker image multi-stage build and export (`visitor-counter:local`) |
| 03 | `03_docker_compose_up.jpg` | Task 1: Containerization | Docker Compose service startup logs showing Redis and Web healthy |
| 04 | `04_docker_compose_running.png` | Task 1: Containerization | `docker compose ps` displaying running containers on `127.0.0.1:8080->8000` |
| 05 | `05_minikube_dual_clusters.png` | Task 2 & 4: Kubernetes Setup | Minikube dual profile verification (`vc-primary` and `vc-backup`) |
| 06 | `06_k8s_pods_services_pvc.jpg` | Task 2: K8s Deployment | Deployment, StatefulSet, Services, Pods, and PersistentVolumeClaim (`Bound` 1Gi) |
| 07 | `07_k8s_running_pods.png` | Task 2: Running Pods | Verification of active running pods across Redis and Flask Web |
| 08 | `08_self_healing_recovery.png` | Task 2: Self-Healing | Pod deletion and automatic recreation: `PASSED self-healing: visitor-xjts8 -> visitor-v5bnq` |
| 09 | `09_metrics_server_resources.png` | Task 3: HPA Metrics | `metrics-server` pod active and `kubectl top pods` reporting CPU & Memory |
| 10 | `10_hpa_initial_state.jpg` | Task 3: HPA Baseline | HorizontalPodAutoscaler initial state (`cpu: <unknown>/60%`, 1 replica) |
| 11 | `11_hpa_load_generation_job.png` | Task 3: Load Testing | Batch load generation job executing 4,864 concurrent requests over 150 seconds |
| 12 | `12_hpa_scale_up_5_replicas.jpg` | Task 3: HPA Scaling | HPA detecting 500% CPU load and scaling deployment from 1 to 5 replicas |
| 13 | `13_hpa_scale_down_cooloff.jpg` | Task 3: HPA Scale-Down | HPA stabilization window cooling off, scaling back from 5 down to 1 replica |
| 14 | `14_hybrid_cloud_contexts.png` | Task 4: Hybrid Cloud | Kubeconfig contexts for `vc-primary` (On-Prem) and `vc-backup` (Simulated Cloud) |
| 15 | `15_hybrid_failover_success.png` | Task 4: Failover Demonstration | Primary node stopped; automatic failover to `Backup simulated public cloud` (HTTP 200) |
