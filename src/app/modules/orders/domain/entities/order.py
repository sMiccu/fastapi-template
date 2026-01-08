"""Order entity (Aggregate Root)."""

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal

from app.modules.orders.domain.entities.order_item import OrderItem
from app.modules.orders.domain.exceptions import (
    EmptyOrderError,
    InvalidQuantityError,
    OrderAlreadyConfirmedError,
    OrderCannotBeCancelledError,
)
from app.modules.orders.domain.value_objects.customer_id import CustomerId
from app.modules.orders.domain.value_objects.order_id import OrderId
from app.modules.orders.domain.value_objects.order_status import OrderStatus
from app.modules.orders.domain.value_objects.product_id import ProductId
from app.shared.domain.value_objects.money import Money


@dataclass
class Order:
    """Order entity (Aggregate Root).

    This is the main entity in the order aggregate. It enforces business rules
    and maintains consistency within the aggregate boundary.

    Attributes:
        id: Order identifier
        customer_id: Customer who placed the order
        status: Current order status
        created_at: When the order was created
    """

    id: OrderId
    customer_id: CustomerId
    status: OrderStatus
    created_at: datetime
    _items: list[OrderItem] = field(default_factory=list)

    @classmethod
    def create(cls, customer_id: CustomerId) -> "Order":
        """Factory method to create a new order.

        Args:
            customer_id: Customer identifier

        Returns:
            New Order instance
        """
        return cls(
            id=OrderId.generate(),
            customer_id=customer_id,
            status=OrderStatus.PENDING,
            created_at=datetime.now(),
        )

    def add_item(
        self,
        product_id: ProductId,
        quantity: int,
        unit_price: Money,
    ) -> None:
        """Add an item to the order.

        Business Rules:
        - Can only add items to pending orders
        - Quantity must be positive

        Args:
            product_id: Product identifier
            quantity: Quantity to order
            unit_price: Price per unit

        Raises:
            OrderAlreadyConfirmedError: If order is not pending
            InvalidQuantityError: If quantity is invalid
        """
        if self.status != OrderStatus.PENDING:
            raise OrderAlreadyConfirmedError()

        if quantity <= 0:
            raise InvalidQuantityError(quantity)

        item = OrderItem(
            product_id=product_id,
            quantity=quantity,
            unit_price=unit_price,
        )
        self._items.append(item)

    def remove_item(self, product_id: ProductId) -> None:
        """Remove an item from the order.

        Business Rules:
        - Can only remove items from pending orders

        Args:
            product_id: Product identifier to remove

        Raises:
            OrderAlreadyConfirmedError: If order is not pending
        """
        if self.status != OrderStatus.PENDING:
            raise OrderAlreadyConfirmedError()

        self._items = [item for item in self._items if item.product_id != product_id]

    def confirm(self) -> None:
        """Confirm the order.

        Business Rules:
        - Can only confirm pending orders
        - Order must have at least one item

        Raises:
            OrderAlreadyConfirmedError: If order is not pending
            EmptyOrderError: If order has no items
        """
        if self.status != OrderStatus.PENDING:
            raise OrderAlreadyConfirmedError()

        if not self._items:
            raise EmptyOrderError()

        self.status = OrderStatus.CONFIRMED

    def cancel(self) -> None:
        """Cancel the order.

        Business Rules:
        - Cannot cancel shipped or delivered orders

        Raises:
            OrderCannotBeCancelledError: If order cannot be cancelled
        """
        if self.status in [OrderStatus.SHIPPED, OrderStatus.DELIVERED]:
            raise OrderCannotBeCancelledError(self.status.value)

        self.status = OrderStatus.CANCELLED

    def mark_as_paid(self) -> None:
        """Mark order as paid.

        Business Rules:
        - Can only mark confirmed orders as paid

        Raises:
            OrderException: If order is not confirmed
        """
        if self.status != OrderStatus.CONFIRMED:
            raise OrderAlreadyConfirmedError()

        self.status = OrderStatus.PAID

    def calculate_total(self) -> Money:
        """Calculate total order amount.

        Returns:
            Total amount for all items in the order
        """
        if not self._items:
            return Money(Decimal("0"))

        total = Money(Decimal("0"), self._items[0].unit_price.currency)
        for item in self._items:
            total = total.add(item.subtotal())
        return total

    @property
    def items(self) -> list[OrderItem]:
        """Get order items (read-only).

        Returns:
            Copy of order items list
        """
        return self._items.copy()

    @property
    def item_count(self) -> int:
        """Get total number of items in the order.

        Returns:
            Number of items
        """
        return len(self._items)

    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return (
            f"Order(id={self.id!r}, "
            f"customer_id={self.customer_id!r}, "
            f"status={self.status!r}, "
            f"items={len(self._items)})"
        )
