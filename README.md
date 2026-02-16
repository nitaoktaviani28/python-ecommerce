# 🐍 Python E-Commerce - Production-Grade with Full Observability

Python FastAPI application that is **architecturally equivalent** to the Golang e-commerce application running on AKS.

## 🎯 Architecture Parity with Golang Application

This Python application mirrors the Golang application's architecture:

| Component | Golang | Python | Status |
|-----------|--------|--------|--------|
| **Framework** | net/http | FastAPI | ✅ |
| **Database** | PostgreSQL (otelsql) | PostgreSQL (SQLAlchemy) | ✅ |
| **Tracing** | OpenTelemetry → Tempo | OpenTelemetry → Tempo | ✅ |
| **Profiling** | Pyroscope | Pyroscope | ✅ |
| **SQL Tracing** | otelsql | SQLAlchemy instrumentation | ✅ |
| **Observability Init** | Single entry point | Single entry point | ✅ |
| **Clean Business Logic** | No observability code | No observability code | ✅ |
| **Templates** | html/template | Jinja2 | ✅ |
| **Deployment** | AKS | AKS | ✅ |

## 📁 Project Structure

```
python-ecommerce/
├── main.py                      # Entry point (equivalent to main.go)
├── handlers/
│   ├── home.py                  # Product listing handler
│   ├── checkout.py              # Order processing handler
│   └── success.py               # Order confirmation handler
├── repository/
│   ├── database.py              # SQLAlchemy setup & models
│   ├── product_repository.py   # Product data access
│   └── order_repository.py     # Order data access
├── observability/
│   ├── init.py                  # Single entry point (equivalent to Init())
│   ├── tracing.py               # OpenTelemetry setup
│   ├── profiling.py             # Pyroscope setup
│   └── env.py                   # Environment utilities
├── templates/
│   ├── index.html               # Product catalog UI
│   └── success.html             # Order success UI
├── requirements.txt             # Python dependencies
└── Dockerfile                   # Container build for AKS
```

## 🔍 Observability Architecture

### Distributed Tracing Flow
```
HTTP Request (FastAPI)
    ↓ [FastAPI Instrumentation]
Handler Execution
    ↓ [Context Propagation]
Repository Call
    ↓ [SQLAlchemy Instrumentation]
SQL Query Execution
    ↓ [OTLP HTTP]
Alloy
    ↓
Grafana Tempo
```

### Key Features

1. **Single Initialization Point**
   ```python
   # main.py
   observability_init(app)  # ONE call, equivalent to observability.Init() in Go
   ```

2. **Automatic SQL Tracing**
   - SQLAlchemy instrumentation traces ALL SQL queries
   - Equivalent to `otelsql` in Golang
   - SQL spans appear as children of HTTP spans in Tempo

3. **Clean Business Logic**
   - Handlers contain NO tracing code
   - Repository contains NO tracing code
   - Observability is transparent

4. **AlwaysOn Sampling**
   - Equivalent to `AlwaysSample` in Go
   - All requests are traced

## 🚀 Deployment to AKS

### Environment Variables

```bash
# Service identification
OTEL_SERVICE_NAME=ecommerce-python

# Tracing endpoint (Alloy)
OTEL_EXPORTER_OTLP_ENDPOINT=http://alloy.monitoring.svc.cluster.local:4318

# Profiling endpoint (Pyroscope)
PYROSCOPE_ENDPOINT=http://pyroscope-distributor.monitoring.svc.cluster.local:4040

# Database connection (EXISTING PostgreSQL)
DATABASE_DSN=postgresql://postgres:postgres@postgres.app.svc.cluster.local:5432/shop
```

### Build & Deploy

```bash
# Build Docker image
docker build -t ecommerce-python:latest .

# Tag for ACR
docker tag ecommerce-python:latest <your-acr>.azurecr.io/ecommerce-python:latest

# Push to ACR
docker push <your-acr>.azurecr.io/ecommerce-python:latest

# Deploy to AKS
kubectl apply -f deployment.yaml
```

### Kubernetes Deployment Example

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ecommerce-python
  namespace: app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: ecommerce-python
  template:
    metadata:
      labels:
        app: ecommerce-python
    spec:
      containers:
      - name: ecommerce-python
        image: <your-acr>.azurecr.io/ecommerce-python:latest
        ports:
        - containerPort: 8080
        env:
        - name: OTEL_SERVICE_NAME
          value: "ecommerce-python"
        - name: OTEL_EXPORTER_OTLP_ENDPOINT
          value: "http://alloy.monitoring.svc.cluster.local:4318"
        - name: PYROSCOPE_ENDPOINT
          value: "http://pyroscope-distributor.monitoring.svc.cluster.local:4040"
        - name: DATABASE_DSN
          value: "postgresql://postgres:postgres@postgres.app.svc.cluster.local:5432/shop"
```

## 🔧 Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DATABASE_DSN="postgresql://postgres:postgres@localhost:5432/shop"
export OTEL_SERVICE_NAME="ecommerce-python-local"
export OTEL_EXPORTER_OTLP_ENDPOINT="http://localhost:4318"

# Run application
python main.py
```

## 📊 Observability Verification

### 1. Verify Tracing in Tempo
- Open Grafana → Explore → Tempo
- Search for service: `ecommerce-python`
- Verify trace structure:
  ```
  GET /
    └── SELECT products (SQLAlchemy)
  
  POST /checkout
    ├── SELECT product (SQLAlchemy)
    └── INSERT order (SQLAlchemy)
  ```

### 2. Verify Profiling in Pyroscope
- Open Pyroscope UI
- Select application: `ecommerce-python`
- Verify CPU profile shows `simulate_cpu_work` function

### 3. Verify Database Connection
```bash
# Check logs
kubectl logs -n app deployment/ecommerce-python

# Should see:
# ✅ Connected to PostgreSQL: postgres.app.svc.cluster.local:5432/shop
# ✅ Tracing initialized (AlwaysOn sampler)
# ✅ SQLAlchemy instrumented (SQL query tracing)
```

## 🎓 Key Architectural Decisions

### 1. SQLAlchemy Instrumentation
- **Why**: Provides automatic SQL query tracing equivalent to `otelsql` in Go
- **Benefit**: Zero code changes in repository layer
- **Result**: SQL queries appear as child spans in distributed traces

### 2. Single Observability Entry Point
- **Why**: Maintains clean separation of concerns
- **Benefit**: Business logic remains framework-agnostic
- **Result**: Easy to test and maintain

### 3. Fail-Graceful Observability
- **Why**: Observability failure should not crash the application
- **Benefit**: Application remains available even if Tempo/Pyroscope is down
- **Result**: Production resilience

### 4. Existing Database Connection
- **Why**: Reuses existing PostgreSQL StatefulSet in Kubernetes
- **Benefit**: No additional infrastructure needed
- **Result**: Cost-effective and consistent with Go app

## 🔄 Migration from Go to Python

If migrating from Go to Python:

1. **Database**: No changes needed (same PostgreSQL)
2. **Observability**: Same endpoints (Alloy, Tempo, Pyroscope)
3. **Traces**: Compatible trace format (OpenTelemetry)
4. **Deployment**: Same Kubernetes namespace and services

## 📈 Performance Considerations

- **Connection Pooling**: SQLAlchemy pool (size=5, max_overflow=10)
- **Async Support**: FastAPI with uvicorn for high concurrency
- **Health Checks**: Built-in health check endpoint
- **Graceful Shutdown**: Database connections closed properly

---

**Production-ready Python application with full observability parity to Golang!** 🚀

