"""
repository/database.py

Database connection management menggunakan SQLAlchemy (2.x).
Connects ke existing PostgreSQL service di Kubernetes.
"""

import os
import logging
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime,
    DECIMAL,
    text,
)
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func

logger = logging.getLogger(__name__)

# =========================
# SQLALCHEMY BASE
# =========================
Base = declarative_base()

# =========================
# DATABASE ENGINE & SESSION
# =========================
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

    DATABASE_DSN format:
    postgresql://postgres:postgres@postgres.app.svc.cluster.local:5432/shop
    """
    global engine, SessionLocal

    database_dsn = os.getenv(
        "DATABASE_DSN",
        "postgresql://postgres:postgres@postgres.app.svc.cluster.local:5432/shop"
    )

    # Create SQLAlchemy engine (2.x compatible)
    engine = create_engine(
        database_dsn,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
        echo=False,
        future=True,  # 🔥 WAJIB untuk SQLAlchemy 2.x
    )

    # Test connection (SQLAlchemy 2.x style)
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))

    # Create session factory
    SessionLocal = sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False,
        future=True,  # 🔥 WAJIB
    )

    logger.info("✅ Connected to PostgreSQL")


def close():
    """Close database connection gracefully"""
    global engine
    if engine:
        engine.dispose()
        logger.info("Database connection closed")


def get_db():
    """
    Dependency provider for database session (FastAPI).

    Yields:
        SQLAlchemy Session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

