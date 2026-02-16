"""
repository/product_repository.py

Product repository untuk data access.
Business logic yang bersih tanpa observability code.
SQL queries akan di-trace otomatis oleh SQLAlchemy instrumentation.
"""

from sqlalchemy.orm import Session
from .database import Product


def get_all_products(db: Session):
    """
    Get all products dari database.
    
    SQL query akan di-trace otomatis sebagai child span.
    Equivalent dengan getProducts() di Go repository.
    
    Args:
        db: SQLAlchemy session
        
    Returns:
        List of Product objects
    """
    return db.query(Product).order_by(Product.id).all()


def get_product_by_id(db: Session, product_id: int):
    """
    Get product by ID.
    
    SQL query akan di-trace otomatis sebagai child span.
    Equivalent dengan getProduct() di Go repository.
    
    Args:
        db: SQLAlchemy session
        product_id: Product ID
        
    Returns:
        Product object or None
    """
    return db.query(Product).filter(Product.id == product_id).first()

