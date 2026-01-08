"""Database configuration and session management."""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import settings

# Create engine
engine = create_engine(
    settings.database_url,
    echo=settings.database_echo,
    pool_pre_ping=True,  # Verify connections before using
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""

    pass


def get_db() -> Generator[Session, None, None]:
    """Dependency to get database session.

    Yields:
        Database session

    Example:
        @router.get("/items")
        def get_items(db: Session = Depends(get_db)):
            return db.query(ItemModel).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
