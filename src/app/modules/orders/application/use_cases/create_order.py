"""Create order use case."""

from uuid import UUID

from app.modules.orders.application.dto.commands import CreateOrderCommand
from app.modules.orders.domain.entities.order import Order
from app.modules.orders.domain.repositories.order_repository import OrderRepository
from app.modules.orders.domain.value_objects.customer_id import CustomerId
from app.modules.orders.domain.value_objects.order_id import OrderId


class CreateOrderUseCase:
    """Use case for creating a new order.

    This use case handles the business flow of creating a new order.
    """

    def __init__(self, order_repository: OrderRepository) -> None:
        """Initialize use case.

        Args:
            order_repository: Order repository
        """
        self.order_repository = order_repository

    def execute(self, command: CreateOrderCommand) -> OrderId:
        """Execute the use case.

        Args:
            command: Create order command

        Returns:
            ID of the created order
        """
        # Convert DTO to domain value object
        customer_id = CustomerId(UUID(command.customer_id))

        # Create domain entity
        order = Order.create(customer_id)

        # Persist
        self.order_repository.save(order)

        return order.id
