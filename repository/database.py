"""
repository/database.py

Database connection management menggunakan SQLAlchemy.
Connects ke existing PostgreSQL service di Kubernetes.
"""

import os
import logging
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

logger = logging.getLogger(__name__)

# SQLAlchemy Base
Base = declarative_base()

# Database engine dan session
engine = None
SessionLocal = None


# =========================
# DATABASE MODELS
# =========================

class Product(Base):
    """Product model - equivalent dengan Product struct di Go"""
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)


class Order(Base):
    """Order model - equivalent dengan Order struct di Go"""
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    total = Column(DECIMAL(10, 2), nullable=False)
    created_at = Column(DateTime, server_default=func.now())


# =========================
# DATABASE INITIALIZATION
# =========================

def init():
    """
    Initialize database connection.
    Connects ke existing PostgreSQL service di Kubernetes.
    
    DATABASE_DSN format:
    postgresql://postgres:postgres@postgres.app.svc.cluster.local:5432/shop
    """
    global engine, SessionLocal
    
    # Get database DSN dari environment variable
    database_dsn = os.getenv(
        "DATABASE_DSN",
        "postgresql://postgres:postgres@postgres.app.svc.cluster.local:5432/shop"
    )
    
    # Create engine dengan connection pooling
    engine = create_engine(
        database_dsn,
        pool_pre_ping=True,  # Verify connections before using
        pool_size=5,
        max_overflow=10,
        echo=False  # Set True untuk debug SQL queries
    )
    
    # Test connection
    with engine.connect() as conn:
        conn.execute("SELECT 1")
    
    # Create session factory
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    logger.info(f"✅ Connected to PostgreSQL: {database_dsn.split('@')[1]}")


def close():
    """Close database connection gracefully"""
    global engine
    if engine:
        engine.dispose()
        logger.info("Database connection closed")


def get_db():
    """
    Get database session.
    Digunakan sebagai dependency di FastAPI handlers.
    
    Yields:
        SQLAlchemy session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

