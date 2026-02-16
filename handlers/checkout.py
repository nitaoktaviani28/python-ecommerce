"""
handlers/checkout.py

Checkout handler untuk memproses order.
Business logic yang bersih tanpa observability code.
Tracing ditangani otomatis oleh FastAPI instrumentation.
"""

import logging
from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from repository.database import get_db
from repository import product_repository, order_repository

logger = logging.getLogger(__name__)

# Create router
router = APIRouter()


@router.post("/checkout")
async def checkout(
    request: Request,
    product_id: int = Form(...),
    quantity: int = Form(...),
    db: Session = Depends(get_db)
):
    """
    Proses checkout dan create order.
    
    Handler ini TIDAK mengandung kode tracing atau profiling.
    - HTTP request di-trace otomatis oleh FastAPI instrumentation
    - SQL queries di-trace otomatis oleh SQLAlchemy instrumentation
    
    Equivalent dengan Checkout handler di Go.
    
    Args:
        request: FastAPI request object
        product_id: Product ID dari form
        quantity: Quantity dari form
        db: Database session (injected)
        
    Returns:
        Redirect ke success page
    """
    # Simulate CPU-intensive work untuk profiling visibility
    simulate_cpu_work()
    
    # Get product dari repository
    # SQL query akan muncul sebagai child span di Tempo
    product = product_repository.get_product_by_id(db, product_id)
    
    if not product:
        logger.error(f"Product not found: {product_id}")
        return {"error": "Product not found"}
    
    # Calculate total
    total = float(product.price) * quantity
    
    # Create order
    # SQL INSERT akan muncul sebagai child span di Tempo
    order = order_repository.create_order(db, product_id, quantity, total)
    
    logger.info(f"Order created: ID={order.id}, Product={product.name}, Total={total}")
    
    # Redirect ke success page
    return RedirectResponse(
        url=f"/success?order_id={order.id}",
        status_code=303
    )


def simulate_cpu_work():
    """
    Simulasi CPU-intensive work untuk profiling visibility.
    Fungsi ini akan terlihat di Pyroscope flamegraph.
    Equivalent dengan simulateCPUWork() di Go.
    """
    result = 0
    for i in range(2000000):
        result += i * i * i
    
    # Simulate memory allocation
    data = [i for i in range(10000)]
    return result

