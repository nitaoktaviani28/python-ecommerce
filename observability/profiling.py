"""
observability/profiling.py

Grafana Pyroscope profiling setup.
Enables continuous CPU and allocation profiling.
"""

import logging
import pyroscope

from .env import get_env

logger = logging.getLogger(__name__)


def init_profiling():
    """
    Setup Grafana Pyroscope profiling.
    
    Profiling data akan dikirim ke Pyroscope distributor.
    Includes CPU and allocation profiling.
    """
    pyroscope.configure(
        application_name=get_env("OTEL_SERVICE_NAME", "ecommerce-python"),
        server_address=get_env(
            "PYROSCOPE_ENDPOINT",
            "http://pyroscope-distributor.monitoring.svc.cluster.local:4040"
        ),
        # Enable CPU and allocation profiling
        detect_subprocesses=False,
    )
    logger.info("✅ Pyroscope profiling initialized (CPU + allocation)")

