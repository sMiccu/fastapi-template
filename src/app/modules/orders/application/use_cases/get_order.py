"""Get order use case."""

from uuid import UUID

from app.modules.orders.domain.entities.order import Order
from app.modules.orders.domain.exceptions import OrderNotFoundException
from app.modules.orders.domain.repositories.order_repository import OrderRepository
from app.modules.orders.domain.value_objects.order_id import OrderId


class GetOrderUseCase:
    """Use case for retrieving an order.

    This is a query use case for reading order data.
    """

    def __init__(self, order_repository: OrderRepository) -> None:
        """Initialize use case.

        Args:
            order_repository: Order repository
        """
        self.order_repository = order_repository

    def execute(self, order_id: str) -> Order:
        """Execute the use case.

        Args:
            order_id: Order ID as string

        Returns:
            Order entity

        Raises:
            OrderNotFoundException: If order not found
        """
        order_id_vo = OrderId(UUID(order_id))
        order = self.order_repository.find_by_id(order_id_vo)

        if not order:
            raise OrderNotFoundException(order_id)

        return order
