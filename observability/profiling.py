"""
observability/profiling.py

Grafana Pyroscope profiling setup for Python.
Enables CPU + memory profiling automatically.
"""

import logging
import pyroscope

from .env import get_env

logger = logging.getLogger(__name__)


def init_profiling():
    try:
        pyroscope.configure(
            application_name=get_env(
                "OTEL_SERVICE_NAME",
                "python-ecommerce"
            ),
            server_address=get_env(
                "PYROSCOPE_ENDPOINT",
                "http://pyroscope-distributor.monitoring.svc.cluster.local:4040"
            ),

            # IMPORTANT
            detect_subprocesses=False,
        )

        logger.info("✅ Pyroscope profiling initialized (CPU + memory)")

    except Exception as e:
        logger.exception("❌ Pyroscope profiling failed")
        raise

