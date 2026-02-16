
"""
repository/order_repository.py

Order repository untuk data access.
Business logic yang bersih tanpa observability code.
SQL queries akan di-trace otomatis oleh SQLAlchemy instrumentation.
"""

from sqlalchemy.orm import Session
from .database import Order


def create_order(db: Session, product_id: int, quantity: int, total: float):
    """
    Create new order di database.
    
    SQL INSERT akan di-trace otomatis sebagai child span.
    Equivalent dengan createOrder() di Go repository.
    
    Args:
        db: SQLAlchemy session
        product_id: Product ID
        quantity: Order quantity
        total: Total price
        
    Returns:
        Created Order object
    """
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
    
    SQL query akan di-trace otomatis sebagai child span.
    Equivalent dengan getOrder() di Go repository.
    
    Args:
        db: SQLAlchemy session
        order_id: Order ID
        
    Returns:
        Order object or None
    """
    return db.query(Order).filter(Order.id == order_id).first()

