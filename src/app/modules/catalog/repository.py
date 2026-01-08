"""Repository for catalog module (concrete implementation)."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.catalog.exceptions import ProductNotFoundException
from app.modules.catalog.models import CategoryModel, ProductModel


class ProductRepository:
    """Repository for Product operations.

    Note: This is a concrete implementation (not an interface)
    because the catalog module uses simple layered architecture.
    """

    def __init__(self, session: Session) -> None:
        """Initialize repository.

        Args:
            session: Database session
        """
        self.session = session

    def find_by_id(self, product_id: UUID) -> ProductModel:
        """Find product by ID.

        Args:
            product_id: Product UUID

        Returns:
            Product model

        Raises:
            ProductNotFoundException: If product not found
        """
        product = self.session.get(ProductModel, product_id)
        if not product:
            raise ProductNotFoundException(str(product_id))
        return product

    def find_all(self, skip: int = 0, limit: int = 100) -> list[ProductModel]:
        """Find all products with pagination.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of product models
        """
        stmt = select(ProductModel).offset(skip).limit(limit)
        result = self.session.execute(stmt)
        return list(result.scalars().all())

    def find_by_category(self, category_id: UUID) -> list[ProductModel]:
        """Find products by category.

        Args:
            category_id: Category UUID

        Returns:
            List of product models
        """
        stmt = select(ProductModel).where(ProductModel.category_id == category_id)
        result = self.session.execute(stmt)
        return list(result.scalars().all())

    def create(self, product: ProductModel) -> ProductModel:
        """Create a new product.

        Args:
            product: Product model to create

        Returns:
            Created product model
        """
        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)
        return product

    def update(self, product: ProductModel) -> ProductModel:
        """Update an existing product.

        Args:
            product: Product model to update

        Returns:
            Updated product model
        """
        self.session.commit()
        self.session.refresh(product)
        return product

    def delete(self, product_id: UUID) -> None:
        """Delete a product.

        Args:
            product_id: Product UUID

        Raises:
            ProductNotFoundException: If product not found
        """
        product = self.find_by_id(product_id)
        self.session.delete(product)
        self.session.commit()


class CategoryRepository:
    """Repository for Category operations."""

    def __init__(self, session: Session) -> None:
        """Initialize repository.

        Args:
            session: Database session
        """
        self.session = session

    def find_all(self) -> list[CategoryModel]:
        """Find all categories.

        Returns:
            List of category models
        """
        stmt = select(CategoryModel)
        result = self.session.execute(stmt)
        return list(result.scalars().all())

    def create(self, category: CategoryModel) -> CategoryModel:
        """Create a new category.

        Args:
            category: Category model to create

        Returns:
            Created category model
        """
        self.session.add(category)
        self.session.commit()
        self.session.refresh(category)
        return category
