#!/usr/bin/env python3
"""
Load Generation Script for Kubernetes HPA Testing.
Sends concurrent HTTP requests to trigger CPU utilization above the 50% target,
causing Horizontal Pod Autoscaler (HPA) to scale out pods from 2 to 4..10 replicas.
"""

import urllib.request
import threading
import time
import sys

URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5000/load?duration=3"
CONCURRENCY = int(sys.argv[2]) if len(sys.argv) > 2 else 10
TOTAL_SECONDS = int(sys.argv[3]) if len(sys.argv) > 3 else 90

stop_flag = False
request_count = 0
success_count = 0

def worker(worker_id):
    global request_count, success_count, stop_flag
    while not stop_flag:
        try:
            req = urllib.request.Request(URL)
            with urllib.request.urlopen(req, timeout=5) as res:
                if res.status == 200:
                    success_count += 1
            request_count += 1
        except Exception:
            request_count += 1
        time.sleep(0.1)

print("=" * 60)
print("  Kubernetes HPA Load Generator")
print(f"  Target URL:    {URL}")
print(f"  Concurrency:   {CONCURRENCY} concurrent threads")
print(f"  Duration:      {TOTAL_SECONDS} seconds")
print("=" * 60)
print("\nOpen a second terminal and monitor scaling with:")
print("  kubectl get hpa visitor-counter-hpa --watch")
print("  kubectl get pods -l app=visitor-counter -w\n")

threads = []
for i in range(CONCURRENCY):
    t = threading.Thread(target=worker, args=(i,))
    t.daemon = True
    t.start()
    threads.append(t)

start_time = time.time()
try:
    while time.time() - start_time < TOTAL_SECONDS:
        elapsed = int(time.time() - start_time)
        print(f"[{elapsed:02d}s/{TOTAL_SECONDS}s] Sent: {request_count} requests | Success: {success_count}", end='\r')
        time.sleep(1)
except KeyboardInterrupt:
    print("\nInterrupted by user.")

stop_flag = True
print(f"\n\nLoad test finished! Total requests: {request_count}, Successful: {success_count}")
print("Check your HPA status: kubectl get hpa visitor-counter-hpa")

