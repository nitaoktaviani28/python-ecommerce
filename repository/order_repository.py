"""
repository/order_repository.py

Order repository untuk data access.
Mengandung MANUAL SPAN agar trace semantik setara dengan Go.
"""

from sqlalchemy.orm import Session
from opentelemetry import trace

from .database import Order

tracer = trace.get_tracer("repository.order")


def create_order(db: Session, product_id: int, quantity: int, total: float):
    """
    Create new order.
    Equivalent dengan createOrder() di Go repository.
    """
    # 🔥 MANUAL SPAN
    with tracer.start_as_current_span("create_order"):
        order = Order(
            product_id=product_id,
            quantity=quantity,
            total=total
        )
        db.add(order)
        db.commit()
        db.refresh(order)
        return order


def get_order_by_id(db: Session, order_id: int):
    """
    Get order by ID.
    Equivalent dengan getOrder() di Go repository.
    """
    # 🔥 MANUAL SPAN
    with tracer.start_as_current_span("get_order"):
        return (
            db.query(Order)
            .filter(Order.id == order_id)
            .first()
        )

