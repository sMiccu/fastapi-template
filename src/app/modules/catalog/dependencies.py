"""Dependency injection for catalog module."""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.catalog.repository import CategoryRepository, ProductRepository
from app.modules.catalog.service import CategoryService, ProductService


def get_product_repository(session: Annotated[Session, Depends(get_db)]) -> ProductRepository:
    """Get product repository instance.

    Args:
        session: Database session

    Returns:
        Product repository
    """
    return ProductRepository(session)


def get_product_service(
    repository: Annotated[ProductRepository, Depends(get_product_repository)],
) -> ProductService:
    """Get product service instance.

    Args:
        repository: Product repository

    Returns:
        Product service
    """
    return ProductService(repository)


def get_category_repository(session: Annotated[Session, Depends(get_db)]) -> CategoryRepository:
    """Get category repository instance.

    Args:
        session: Database session

    Returns:
        Category repository
    """
    return CategoryRepository(session)


def get_category_service(
    repository: Annotated[CategoryRepository, Depends(get_category_repository)],
) -> CategoryService:
    """Get category service instance.

    Args:
        repository: Category repository

    Returns:
        Category service
    """
    return CategoryService(repository)
