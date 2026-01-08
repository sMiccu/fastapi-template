"""Order repository interface (Port)."""

from abc import ABC, abstractmethod

from app.modules.orders.domain.entities.order import Order
from app.modules.orders.domain.value_objects.customer_id import CustomerId
from app.modules.orders.domain.value_objects.order_id import OrderId


class OrderRepository(ABC):
    """Repository interface for Order aggregate.

    This is a Port in hexagonal architecture - defines what we need,
    but doesn't specify how it's implemented.
    """

    @abstractmethod
    def find_by_id(self, order_id: OrderId) -> Order | None:
        """Find an order by its ID.

        Args:
            order_id: Order identifier

        Returns:
            Order entity or None if not found
        """
        pass

    @abstractmethod
    def find_by_customer(self, customer_id: CustomerId) -> list[Order]:
        """Find all orders for a customer.

        Args:
            customer_id: Customer identifier

        Returns:
            List of Order entities
        """
        pass

    @abstractmethod
    def save(self, order: Order) -> None:
        """Save an order.

        Args:
            order: Order entity to save
        """
        pass

    @abstractmethod
    def delete(self, order_id: OrderId) -> None:
        """Delete an order.

        Args:
            order_id: Order identifier
        """
        pass

    @abstractmethod
    def next_id(self) -> OrderId:
        """Generate next order ID.

        Returns:
            New OrderId
        """
        pass
