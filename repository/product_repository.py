"""
repository/product_repository.py

Product repository untuk data access.
Mengandung MANUAL SPAN agar trace semantik setara dengan Go.
"""

from sqlalchemy.orm import Session
from opentelemetry import trace

from .database import Product

# Tracer khusus repository (BEST PRACTICE)
tracer = trace.get_tracer("repository.product")


def get_all_products(db: Session):
    """
    Get all products dari database.
    Equivalent dengan getProducts() di Go repository.
    """
    # 🔥 MANUAL SPAN (SETARA Go: tracer.Start(ctx, "get_products"))
    with tracer.start_as_current_span("get_products"):
        return db.query(Product).order_by(Product.id).all()


def get_product_by_id(db: Session, product_id: int):
    """
    Get product by ID.
    Equivalent dengan getProduct() di Go repository.
    """
    # 🔥 MANUAL SPAN
    with tracer.start_as_current_span("get_product"):
        return (
            db.query(Product)
            .filter(Product.id == product_id)
            .first()
        )

