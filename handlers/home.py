"""
handlers/home.py

Home page handler untuk menampilkan product list.
Business logic yang bersih tanpa observability code.
Tracing ditangani otomatis oleh FastAPI instrumentation.
"""

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from repository.database import get_db
from repository import product_repository

# Setup Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Create router
router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    """
    Menampilkan halaman utama dengan daftar produk.
    
    Handler ini TIDAK mengandung kode tracing atau profiling.
    - HTTP request di-trace otomatis oleh FastAPI instrumentation
    - SQL queries di-trace otomatis oleh SQLAlchemy instrumentation
    
    Equivalent dengan Home handler di Go.
    
    Args:
        request: FastAPI request object
        db: Database session (injected)
        
    Returns:
        HTML response dengan product list
    """
    # Get products dari repository
    # SQL query akan muncul sebagai child span di Tempo
    products = product_repository.get_all_products(db)
    
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "products": products}
    )

