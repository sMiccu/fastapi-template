"""Order repository implementation (Adapter)."""

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.modules.orders.domain.entities.order import Order
from app.modules.orders.domain.entities.order_item import OrderItem
from app.modules.orders.domain.repositories.order_repository import OrderRepository
from app.modules.orders.domain.value_objects.customer_id import CustomerId
from app.modules.orders.domain.value_objects.order_id import OrderId
from app.modules.orders.domain.value_objects.order_status import OrderStatus
from app.modules.orders.domain.value_objects.product_id import ProductId
from app.modules.orders.infrastructure.persistence.models import (
    OrderItemModel,
    OrderModel,
)
from app.shared.domain.value_objects.money import Money


class OrderRepositoryImpl(OrderRepository):
    """SQLAlchemy implementation of OrderRepository.

    This is an Adapter in hexagonal architecture - it adapts the domain
    repository interface to a specific infrastructure (PostgreSQL via SQLAlchemy).
    """

    def __init__(self, session: Session) -> None:
        """Initialize repository.

        Args:
            session: SQLAlchemy session
        """
        self.session = session

    def find_by_id(self, order_id: OrderId) -> Order | None:
        """Find an order by its ID.

        Args:
            order_id: Order identifier

        Returns:
            Order entity or None if not found
        """
        stmt = (
            select(OrderModel)
            .where(OrderModel.id == order_id.value)
            .options(selectinload(OrderModel.items))  # Eager load items
        )
        result = self.session.execute(stmt)
        model = result.scalar_one_or_none()

        return self._to_entity(model) if model else None

    def find_by_customer(self, customer_id: CustomerId) -> list[Order]:
        """Find all orders for a customer.

        Args:
            customer_id: Customer identifier

        Returns:
            List of Order entities
        """
        stmt = (
            select(OrderModel)
            .where(OrderModel.customer_id == customer_id.value)
            .options(selectinload(OrderModel.items))
        )
        result = self.session.execute(stmt)
        models = result.scalars().all()

        return [self._to_entity(model) for model in models]

    def save(self, order: Order) -> None:
        """Save an order.

        Args:
            order: Order entity to save
        """
        # Check if order already exists
        existing = self.session.get(OrderModel, order.id.value)

        if existing:
            # Update existing order
            self._update_model(existing, order)
        else:
            # Create new order
            model = self._to_model(order)
            self.session.add(model)

        self.session.commit()

    def delete(self, order_id: OrderId) -> None:
        """Delete an order.

        Args:
            order_id: Order identifier
        """
        model = self.session.get(OrderModel, order_id.value)
        if model:
            self.session.delete(model)
            self.session.commit()

    def next_id(self) -> OrderId:
        """Generate next order ID.

        Returns:
            New OrderId
        """
        return OrderId.generate()

    def _to_entity(self, model: OrderModel) -> Order:
        """Convert ORM model to domain entity.

        Args:
            model: SQLAlchemy model

        Returns:
            Domain entity
        """
        # Create order entity
        from decimal import Decimal
        from uuid import UUID as PyUUID

        order = Order(
            id=OrderId(PyUUID(str(model.id))),
            customer_id=CustomerId(PyUUID(str(model.customer_id))),
            status=OrderStatus(model.status),
            created_at=model.created_at,
        )

        # Add items to order (directly to private field to bypass business rules)
        order._items = [
            OrderItem(
                product_id=ProductId(PyUUID(str(item.product_id))),
                quantity=item.quantity,
                unit_price=Money(Decimal(str(item.unit_price)), item.currency),
            )
            for item in model.items
        ]

        return order

    def _to_model(self, entity: Order) -> OrderModel:
        """Convert domain entity to ORM model.

        Args:
            entity: Domain entity

        Returns:
            SQLAlchemy model
        """
        model = OrderModel(
            id=entity.id.value,
            customer_id=entity.customer_id.value,
            status=entity.status.value,
            created_at=entity.created_at,
        )

        # Add order items
        model.items = [
            OrderItemModel(
                product_id=item.product_id.value,
                quantity=item.quantity,
                unit_price=item.unit_price.amount,
                currency=item.unit_price.currency,
            )
            for item in entity.items
        ]

        return model

    def _update_model(self, model: OrderModel, entity: Order) -> None:
        """Update existing ORM model from domain entity.

        Args:
            model: Existing SQLAlchemy model
            entity: Domain entity with updated data
        """
        model.status = entity.status.value

        # Update items - simple approach: delete all and recreate
        model.items.clear()
        for item in entity.items:
            model.items.append(
                OrderItemModel(
                    product_id=item.product_id.value,
                    quantity=item.quantity,
                    unit_price=item.unit_price.amount,
                    currency=item.unit_price.currency,
                )
            )
