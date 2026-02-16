"""
observability/init.py

Single entry point untuk inisialisasi observability.
Fungsi init() dipanggil sekali saat aplikasi startup.
Equivalent dengan observability.Init() di Golang.
"""

import logging
from fastapi import FastAPI

from .tracing import init_tracing
from .profiling import init_profiling

logger = logging.getLogger(__name__)


def init(app: FastAPI):
    """
    Inisialisasi semua komponen observability.
    
    Fungsi ini adalah SATU-SATUNYA titik masuk untuk setup observability.
    Business logic tidak perlu tahu detail implementasi tracing atau profiling.
    
    Observability failure TIDAK akan crash aplikasi (fail gracefully).
    
    Args:
        app: FastAPI application instance
    """
    logger.info("🔍 Initializing observability...")
    
    # Initialize tracing (OpenTelemetry → Tempo via Alloy)
    try:
        init_tracing(app)
    except Exception as e:
        logger.error(f"Tracing init failed (non-fatal): {e}")
    
    # Initialize profiling (Pyroscope)
    try:
        init_profiling()
    except Exception as e:
        logger.error(f"Profiling init failed (non-fatal): {e}")
    
    logger.info("✅ Observability initialized")

