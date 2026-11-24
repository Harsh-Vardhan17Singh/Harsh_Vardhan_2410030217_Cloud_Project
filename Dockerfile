# Multi-stage / Slim Optimized Production Dockerfile
# Technique 3 (Cost Optimization): Reduced attack surface, faster cold starts, 80%+ smaller image size
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build dependencies if needed
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Final runtime image
FROM python:3.11-slim

WORKDIR /app

# Create a non-root security user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy installed Python packages from builder stage
COPY --from=builder /root/.local /home/appuser/.local
ENV PATH=/home/appuser/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

# Copy application source code
COPY --chown=appuser:appuser app.py .
COPY --chown=appuser:appuser templates/ ./templates/

USER appuser

EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/healthz')" || exit 1

# Run with Gunicorn production WSGI server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--threads", "2", "app:app"]

