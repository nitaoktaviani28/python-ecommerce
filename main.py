"""
main.py

Entry point aplikasi e-commerce Python.
Arsitektur ini equivalent dengan aplikasi Golang:
- Single observability initialization point
- Clean separation between business logic and observability
- Database connection dengan tracing ke SQL query level
"""

import logging
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from handlers import home, checkout, success
from observability.init import init as observability_init
from repository import database

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# =========================
# INISIALISASI APLIKASI
# =========================
app = FastAPI(title="E-Commerce Python")

# =========================
# INISIALISASI OBSERVABILITY
# =========================
# Fungsi init() merupakan single entry point untuk mengaktifkan
# tracing, profiling, dan metrics.
# Pendekatan ini menjaga agar logika bisnis tidak bergantung
# langsung pada detail implementasi observability.
observability_init(app)

# =========================
# INISIALISASI DATABASE
# =========================
# Membuka koneksi database dan melakukan validasi koneksi.
# Jika inisialisasi gagal, aplikasi akan dihentikan (fail fast).
@app.on_event("startup")
async def startup_event():
    try:
        database.init()
        logger.info("✅ Database initialized")
    except Exception as e:
        logger.error(f"❌ Database init failed: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    database.close()
    logger.info("Database connection closed")

# =========================
# REGISTRASI HTTP ROUTES
# =========================
# Endpoint aplikasi utama
app.include_router(home.router)
app.include_router(checkout.router)
app.include_router(success.router)

if __name__ == "__main__":
    # =========================
    # MENJALANKAN HTTP SERVER
    # =========================
    # Aplikasi akan mendengarkan request pada port 8080.
    logger.info("🚀 E-commerce Python app starting on :8080")
    uvicorn.run(app, host="0.0.0.0", port=8080)

