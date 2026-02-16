"""
observability/init.py

Single entry point untuk inisialisasi observability.
Dipanggil SATU KALI saat aplikasi startup.

Equivalent dengan observability.Init() di Golang.
"""

import logging
from fastapi import FastAPI

from .tracing import init_tracing
from .profiling import init_profiling

logger = logging.getLogger("observability")


def init(app: FastAPI):
    """
    Inisialisasi seluruh komponen observability.

    - Tracing (OpenTelemetry → Alloy → Tempo)
    - Profiling (Grafana Pyroscope)

    ⚠️ Failure observability TIDAK BOLEH menghentikan aplikasi.
    """

    logger.info("🔍 Initializing observability...")

    # =========================
    # TRACING (OpenTelemetry)
    # =========================
    try:
        init_tracing(app)
        logger.info("✅ Tracing initialized")
    except Exception as exc:
        # Fail gracefully (SAMA seperti Go)
        logger.exception(
            "❌ Tracing initialization failed (non-fatal): %s",
            exc,
        )

    # =========================
    # PROFILING (Pyroscope)
    # =========================
    try:
        init_profiling()
        logger.info("✅ Profiling initialized")
    except Exception as exc:
        # Profiling optional, jangan crash app
        logger.exception(
            "❌ Profiling initialization failed (non-fatal): %s",
            exc,
        )

    logger.info("🚀 Observability setup completed")

