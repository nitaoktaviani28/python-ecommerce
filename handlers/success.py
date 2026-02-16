"""
handlers/success.py

Success page handler untuk menampilkan order confirmation.
Business logic yang bersih tanpa observability code.
Tracing ditangani otomatis oleh FastAPI instrumentation.
"""

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from repository.database import get_db
from repository import order_repository, product_repository

# Setup Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Create router
router = APIRouter()


@router.get("/success", response_class=HTMLResponse)
async def success(
    request: Request,
    order_id: int,
    db: Session = Depends(get_db)
):
    """
    Menampilkan halaman sukses dengan order details.
    
    Handler ini TIDAK mengandung kode tracing atau profiling.
    - HTTP request di-trace otomatis oleh FastAPI instrumentation
    - SQL queries di-trace otomatis oleh SQLAlchemy instrumentation
    
    Equivalent dengan Success handler di Go.
    
    Args:
        request: FastAPI request object
        order_id: Order ID dari query parameter
        db: Database session (injected)
        
    Returns:
        HTML response dengan order details
    """
    # Get order dari repository
    # SQL query akan muncul sebagai child span di Tempo
    order = order_repository.get_order_by_id(db, order_id)
    
    if not order:
        return {"error": "Order not found"}
    
    # Get product details
    # SQL query akan muncul sebagai child span di Tempo
    product = product_repository.get_product_by_id(db, order.product_id)
    
    return templates.TemplateResponse(
        "success.html",
        {
            "request": request,
            "order": order,
            "product": product
        }
    )

