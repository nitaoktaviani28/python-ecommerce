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
from opentelemetry.sdk.trace.sampling import ALWAYS_ON

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

from .env import get_env

logger = logging.getLogger(__name__)


def init_tracing(app: FastAPI):
    """
    Setup OpenTelemetry tracing dengan OTLP HTTP exporter.

    - HTTP tracing via FastAPI instrumentation
    - SQL query tracing via SQLAlchemy instrumentation
    - Always-on sampling (equivalent dengan Go sdktrace.AlwaysSample())
    """

    # =========================
    # RESOURCE (SERVICE ID)
    # =========================
    resource = Resource(attributes={
        ResourceAttributes.SERVICE_NAME: get_env(
            "OTEL_SERVICE_NAME",
            "python-ecommerce"
        )
    })

    # =========================
    # TRACER PROVIDER
    # =========================
    provider = TracerProvider(
        resource=resource,
        sampler=ALWAYS_ON  # ✅ BENAR untuk Python
    )

    # =========================
    # OTLP HTTP EXPORTER
    # =========================
    # ⚠️ HTTP exporter TIDAK mendukung `insecure=True`
    exporter = OTLPSpanExporter(
        endpoint=get_env(
            "OTEL_EXPORTER_OTLP_ENDPOINT",
            "http://alloy.monitoring.svc.cluster.local:4318/v1/traces"
        )
    )

    provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)

    # =========================
    # INSTRUMENTATION
    # =========================
    # HTTP (FastAPI)
    FastAPIInstrumentor.instrument_app(app)

    # SQL (SQLAlchemy)
    SQLAlchemyInstrumentor().instrument()

    logger.info("✅ OpenTelemetry tracing initialized")
    logger.info("✅ Sampler: ALWAYS_ON (100% traces)")
    logger.info("✅ FastAPI HTTP tracing enabled")
    logger.info("✅ SQLAlchemy query tracing enabled")

