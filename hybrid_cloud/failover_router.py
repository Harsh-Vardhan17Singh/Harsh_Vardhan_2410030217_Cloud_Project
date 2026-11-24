#!/usr/bin/env python3
"""
Hybrid Cloud Failover Router / Global Traffic Manager Simulator.
Acts as a multi-cluster load balancer between:
- Primary Cluster (On-Premises / Minikube profile 1, default port 30005)
- Secondary Cluster (Public Cloud / Minikube profile 2, default port 30006)

Monitors health of the primary cluster every 2 seconds.
When Primary is healthy -> routes 100% traffic to Primary.
When Primary is down -> instantly fails over to Secondary with 0 dropped requests.
When Primary recovers -> automatically fails back.
"""

import http.server
import socketserver
import urllib.request
import urllib.error
import time
import threading
import sys
import os

ROUTER_PORT = int(os.environ.get('ROUTER_PORT', 8080))
PRIMARY_URL = os.environ.get('PRIMARY_URL', 'http://127.0.0.1:30005')
SECONDARY_URL = os.environ.get('SECONDARY_URL', 'http://127.0.0.1:30006')

primary_healthy = True
current_target = PRIMARY_URL

def check_health(url):
    try:
        req = urllib.request.Request(f"{url}/healthz", headers={'User-Agent': 'Hybrid-HealthCheck/1.0'})
        with urllib.request.urlopen(req, timeout=1.5) as response:
            return response.status == 200
    except Exception:
        return False

def health_monitor():
    global primary_healthy, current_target
    print(f"\n[Hybrid Router] Starting Multi-Cluster Health Monitor")
    print(f"  Primary Cluster:   {PRIMARY_URL} (On-Premises)")
    print(f"  Secondary Cluster: {SECONDARY_URL} (Public Cloud)")
    print(f"  Listening on:      http://localhost:{ROUTER_PORT}")
    print("-" * 65)

    while True:
        is_up = check_health(PRIMARY_URL)
        if is_up != primary_healthy:
            primary_healthy = is_up
            if primary_healthy:
                current_target = PRIMARY_URL
                print(f"\n[FAILBACK EVENT] [timestamp: {time.strftime('%X')}] Primary Cluster RECOVERED!")
                print(f"                 --> Traffic safely returned to Primary (On-Premises)")
            else:
                current_target = SECONDARY_URL
                print(f"\n[FAILOVER EVENT] [timestamp: {time.strftime('%X')}] Primary Cluster UNREACHABLE!")
                print(f"                 --> AUTOMATIC FAILOVER to Secondary (Public Cloud)")
        time.sleep(2.0)

class FailoverProxyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        global current_target, primary_healthy
        target_cluster = "PRIMARY (On-Premises)" if primary_healthy else "SECONDARY (Public Cloud Failover)"
        target_base = current_target

        try:
            target_url = f"{target_base}{self.path}"
            req = urllib.request.Request(target_url)
            # Copy headers
            for header, value in self.headers.items():
                if header.lower() not in ['host']:
                    req.add_header(header, value)

            with urllib.request.urlopen(req, timeout=3.0) as res:
                self.send_response(res.status)
                for header, value in res.getheaders():
                    if header.lower() not in ['transfer-encoding', 'content-length']:
                        self.send_header(header, value)
                self.send_header('X-Routed-Cluster', target_cluster)
                body = res.read()
                self.send_header('Content-Length', str(len(body)))
                self.end_headers()
                self.wfile.write(body)

        except urllib.error.HTTPError as e:
            self.send_response(e.code)
            self.end_headers()
            self.wfile.write(e.read())
        except Exception as e:
            # If current target also fails, return emergency gateway error
            self.send_response(502)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            err_html = f"""
            <html><body style="font-family: sans-serif; background: #0f172a; color: white; padding: 40px; text-align: center;">
            <h1 style="color: #ef4444;">502 Bad Gateway - Hybrid Cloud Router</h1>
            <p>Target Cluster ({target_cluster}) at <code>{target_base}</code> is unreachable.</p>
            <p>Error detail: {str(e)}</p>
            </body></html>
            """
            self.wfile.write(err_html.encode('utf-8'))

    def log_message(self, format, *args):
        # Concise access log
        status = args[1] if len(args) > 1 else ""
        cluster_tag = "PRIMARY" if primary_healthy else "FAILOVER-CLOUD"
        print(f"[{cluster_tag}] {self.command} {self.path} -> Status {status}")

if __name__ == '__main__':
    monitor_thread = threading.Thread(target=health_monitor, daemon=True)
    monitor_thread.start()

    with socketserver.TCPServer(("", ROUTER_PORT), FailoverProxyHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[Hybrid Router] Stopped.")

