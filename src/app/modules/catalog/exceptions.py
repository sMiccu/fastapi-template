"""Catalog-specific exceptions."""

from app.shared.exceptions import DomainException, NotFoundException


class CatalogException(DomainException):
    """Base exception for catalog module."""

    pass


class ProductNotFoundException(NotFoundException):
    """Raised when a product is not found."""

    def __init__(self, product_id: str) -> None:
        super().__init__(f"Product not found: {product_id}")


class CategoryNotFoundException(NotFoundException):
    """Raised when a category is not found."""

    def __init__(self, category_id: str) -> None:
        super().__init__(f"Category not found: {category_id}")


class InsufficientStockError(CatalogException):
    """Raised when there is insufficient stock."""

    def __init__(self, product_id: str, requested: int, available: int) -> None:
        super().__init__(
            f"Insufficient stock for product {product_id}: "
            f"requested {requested}, available {available}"
        )
