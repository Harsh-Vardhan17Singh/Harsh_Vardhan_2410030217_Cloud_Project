import os
import time
import socket
import math
import redis
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Configuration from environment variables
REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')
REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
REDIS_DB = int(os.environ.get('REDIS_DB', 0))
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', None)
CLUSTER_NAME = os.environ.get('CLUSTER_NAME', 'Primary-Cluster-OnPrem')
APP_ENV = os.environ.get('APP_ENV', 'production')

def get_redis_client():
    return redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB,
        password=REDIS_PASSWORD,
        socket_connect_timeout=2,
        socket_timeout=2,
        decode_responses=True
    )

@app.route('/')
def index():
    hostname = socket.gethostname()
    host_ip = socket.gethostbyname(hostname) if hostname else "127.0.0.1"
    
    count = "Unavailable"
    redis_status = "Disconnected"
    
    try:
        r = get_redis_client()
        count = r.incr('visitor_count')
        redis_status = "Connected (Healthy)"
    except Exception as e:
        redis_status = f"Error: {str(e)}"
        count = "Error connecting to Redis"

    return render_template(
        'index.html',
        count=count,
        hostname=hostname,
        host_ip=host_ip,
        cluster_name=CLUSTER_NAME,
        redis_status=redis_status,
        app_env=APP_ENV
    )

@app.route('/healthz')
def liveness():
    """Kubernetes Liveness Probe"""
    return jsonify({
        "status": "healthy",
        "pod": socket.gethostname(),
        "cluster": CLUSTER_NAME
    }), 200

@app.route('/readyz')
def readiness():
    """Kubernetes Readiness Probe (checks Redis connection)"""
    try:
        r = get_redis_client()
        r.ping()
        return jsonify({
            "status": "ready",
            "redis": "connected",
            "cluster": CLUSTER_NAME
        }), 200
    except Exception as e:
        return jsonify({
            "status": "unready",
            "redis_error": str(e),
            "cluster": CLUSTER_NAME
        }), 503

@app.route('/load')
def generate_load():
    """
    Simulate CPU-intensive computation to trigger Kubernetes HPA (Horizontal Pod Autoscaler).
    Accepts 'duration' parameter in seconds (default 5 seconds).
    """
    duration = float(request.args.get('duration', 4.0))
    start_time = time.time()
    # Compute heavy math operations to spike CPU utilization
    x = 0.0001
    while time.time() - start_time < duration:
        x += math.sqrt(x) * math.sin(x)
        if x > 1000000:
            x = 0.0001

    return jsonify({
        "message": f"Simulated CPU load completed for {duration} seconds",
        "pod": socket.gethostname(),
        "cluster": CLUSTER_NAME
    }), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

