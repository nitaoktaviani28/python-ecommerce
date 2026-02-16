"""
handlers/checkout.py

Checkout handler.
Mengandung MANUAL SPAN agar setara dengan Go handler.
"""

import logging
from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from opentelemetry import trace

from repository.database import get_db
from repository import product_repository, order_repository

logger = logging.getLogger(__name__)

router = APIRouter()

# Tracer khusus handler
tracer = trace.get_tracer("handlers.checkout")


@router.post("/checkout")
async def checkout(
    request: Request,
    product_id: int = Form(...),
    quantity: int = Form(...),
    db: Session = Depends(get_db)
):
    """
    Proses checkout.
    Equivalent dengan Checkout handler di Go.
    """
    # 🔥 MANUAL HANDLER SPAN (SETARA Go: checkout_handler)
    with tracer.start_as_current_span("checkout_handler"):
        simulate_cpu_work()

        # Repository span → DB span
        product = product_repository.get_product_by_id(db, product_id)
        if not product:
            logger.error(f"Product not found: {product_id}")
            return {"error": "Product not found"}

        total = float(product.price) * quantity

        # Repository span → DB span
        order = order_repository.create_order(db, product_id, quantity, total)

        logger.info(
            f"Order created: ID={order.id}, Product={product.name}, Total={total}"
        )

        return RedirectResponse(
            url=f"/success?order_id={order.id}",
            status_code=303
        )


def simulate_cpu_work():
    """
    CPU & memory load simulation.
    Akan muncul di Pyroscope flamegraph.
    """
    result = 0
    for i in range(2_000_000):
        result += i * i * i

    _ = [i for i in range(10_000)]
    return result

