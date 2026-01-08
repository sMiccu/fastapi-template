"""Service layer for catalog module."""

from uuid import UUID

from app.modules.catalog.exceptions import InsufficientStockError
from app.modules.catalog.models import CategoryModel, ProductModel
from app.modules.catalog.repository import CategoryRepository, ProductRepository
from app.modules.catalog.schemas import CategoryCreate, ProductCreate, ProductUpdate


class ProductService:
    """Service for product operations.

    Contains business logic for product management.
    """

    def __init__(self, repository: ProductRepository) -> None:
        """Initialize service.

        Args:
            repository: Product repository
        """
        self.repository = repository

    def get_product(self, product_id: UUID) -> ProductModel:
        """Get a product by ID.

        Args:
            product_id: Product UUID

        Returns:
            Product model
        """
        return self.repository.find_by_id(product_id)

    def list_products(self, skip: int = 0, limit: int = 100) -> list[ProductModel]:
        """List all products.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of product models
        """
        return self.repository.find_all(skip, limit)

    def list_products_by_category(self, category_id: UUID) -> list[ProductModel]:
        """List products by category.

        Args:
            category_id: Category UUID

        Returns:
            List of product models
        """
        return self.repository.find_by_category(category_id)

    def create_product(self, product_data: ProductCreate) -> ProductModel:
        """Create a new product.

        Args:
            product_data: Product creation data

        Returns:
            Created product model
        """
        product = ProductModel(
            name=product_data.name,
            description=product_data.description,
            price=product_data.price,
            currency=product_data.currency,
            category_id=product_data.category_id,
            stock_quantity=product_data.stock_quantity,
            is_active=product_data.is_active,
        )
        return self.repository.create(product)

    def update_product(self, product_id: UUID, product_data: ProductUpdate) -> ProductModel:
        """Update an existing product.

        Args:
            product_id: Product UUID
            product_data: Product update data

        Returns:
            Updated product model
        """
        product = self.repository.find_by_id(product_id)

        # Update only provided fields
        if product_data.name is not None:
            product.name = product_data.name
        if product_data.description is not None:
            product.description = product_data.description
        if product_data.price is not None:
            product.price = product_data.price
        if product_data.currency is not None:
            product.currency = product_data.currency
        if product_data.category_id is not None:
            product.category_id = product_data.category_id
        if product_data.stock_quantity is not None:
            product.stock_quantity = product_data.stock_quantity
        if product_data.is_active is not None:
            product.is_active = product_data.is_active

        return self.repository.update(product)

    def delete_product(self, product_id: UUID) -> None:
        """Delete a product.

        Args:
            product_id: Product UUID
        """
        self.repository.delete(product_id)

    def reduce_stock(self, product_id: UUID, quantity: int) -> ProductModel:
        """Reduce product stock.

        This is a business logic method that ensures stock availability.

        Args:
            product_id: Product UUID
            quantity: Quantity to reduce

        Returns:
            Updated product model

        Raises:
            InsufficientStockError: If insufficient stock
        """
        product = self.repository.find_by_id(product_id)

        if product.stock_quantity < quantity:
            raise InsufficientStockError(str(product_id), quantity, product.stock_quantity)

        product.stock_quantity -= quantity
        return self.repository.update(product)

    def is_available(self, product_id: UUID) -> bool:
        """Check if product is available.

        Args:
            product_id: Product UUID

        Returns:
            True if product is active and has stock
        """
        product = self.repository.find_by_id(product_id)
        return product.is_active and product.stock_quantity > 0


class CategoryService:
    """Service for category operations."""

    def __init__(self, repository: CategoryRepository) -> None:
        """Initialize service.

        Args:
            repository: Category repository
        """
        self.repository = repository

    def list_categories(self) -> list[CategoryModel]:
        """List all categories.

        Returns:
            List of category models
        """
        return self.repository.find_all()

    def create_category(self, category_data: CategoryCreate) -> CategoryModel:
        """Create a new category.

        Args:
            category_data: Category creation data

        Returns:
            Created category model
        """
        category = CategoryModel(
            name=category_data.name,
            slug=category_data.slug,
            parent_id=category_data.parent_id,
        )
        return self.repository.create(category)
