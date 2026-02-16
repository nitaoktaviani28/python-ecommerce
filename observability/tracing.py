"""
observability/tracing.py

OpenTelemetry tracing setup.
Exports traces via OTLP HTTP to Grafana Tempo through Alloy.
Instruments FastAPI (HTTP) and SQLAlchemy (SQL queries).
"""

import logging
from fastapi import FastAPI

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.semconv.resource import ResourceAttributes
from opentelemetry.sdk.trace.sampling import AlwaysOn
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

from .env import get_env

logger = logging.getLogger(__name__)


def init_tracing(app: FastAPI):
    """
    Setup OpenTelemetry tracing dengan OTLP HTTP exporter.
    
    Instrumentasi:
    - FastAPI: HTTP request/response tracing
    - SQLAlchemy: SQL query tracing (equivalent dengan otelsql di Go)
    
    Traces akan dikirim ke Alloy, kemudian diteruskan ke Tempo.
    Menggunakan AlwaysOn sampler (equivalent dengan AlwaysSample di Go).
    """
    # Create resource dengan service name dari environment variable
    resource = Resource(attributes={
        ResourceAttributes.SERVICE_NAME: get_env("OTEL_SERVICE_NAME", "ecommerce-python")
    })
    
    # Create OTLP exporter
    otlp_endpoint = get_env(
        "OTEL_EXPORTER_OTLP_ENDPOINT",
        "http://alloy.monitoring.svc.cluster.local:4318"
    )
    exporter = OTLPSpanExporter(
        endpoint=f"{otlp_endpoint}/v1/traces",
        timeout=10
    )
    
    # Setup tracer provider dengan AlwaysOn sampler
    provider = TracerProvider(
        resource=resource,
        sampler=AlwaysOn()  # Equivalent dengan AlwaysSample di Go
    )
    processor = BatchSpanProcessor(exporter)
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)
    
    # Instrument FastAPI automatically (HTTP tracing)
    FastAPIInstrumentor.instrument_app(app)
    
    # Instrument SQLAlchemy (SQL query tracing)
    # Ini akan membuat span untuk setiap SQL query
    # Equivalent dengan otelsql di Golang
    SQLAlchemyInstrumentor().instrument()
    
    logger.info(f"✅ Tracing initialized (AlwaysOn sampler), sending to: {otlp_endpoint}")
    logger.info("✅ FastAPI instrumented (HTTP tracing)")
    logger.info("✅ SQLAlchemy instrumented (SQL query tracing)")

