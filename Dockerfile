# Production-grade Dockerfile untuk AKS deployment
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements dan install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Environment variables (akan di-override oleh Kubernetes)
ENV OTEL_SERVICE_NAME=ecommerce-python
ENV OTEL_EXPORTER_OTLP_ENDPOINT=http://alloy.monitoring.svc.cluster.local:4318
ENV PYROSCOPE_ENDPOINT=http://pyroscope-distributor.monitoring.svc.cluster.local:4040
ENV DATABASE_DSN=postgresql://postgres:postgres@postgres.app.svc.cluster.local:5432/shop

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8080/')"

# Run application
CMD ["python", "main.py"]

