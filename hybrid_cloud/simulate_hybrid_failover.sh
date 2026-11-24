#!/usr/bin/env bash
# Bash Hybrid Cloud Failover Simulation Script

echo "=========================================================="
echo "   HYBRID CLOUD WITH AUTOMATED FAILOVER SIMULATION       "
echo "=========================================================="

ROUTER_URL="http://localhost:8080"

echo ""
echo "[Step 1] Sending 5 requests to check active cluster:"
for i in {1..5}; do
    curl -s "$ROUTER_URL/healthz" | grep -o '"cluster":"[^"]*"'
    sleep 0.5
done

echo ""
echo "[Step 2] Triggering simulated outage on Primary..."
echo "Run: kubectl scale deployment visitor-counter-web --replicas=0"
sleep 3

echo ""
echo "[Step 3] Sending requests during outage (Traffic automatically fails over to Cloud):"
for i in {1..5}; do
    curl -s "$ROUTER_URL/healthz" | grep -o '"cluster":"[^"]*"'
    sleep 0.5
done

echo ""
echo "[Step 4] Restore Primary:"
echo "Run: kubectl scale deployment visitor-counter-web --replicas=2"

