"""Confirm order use case."""

from uuid import UUID

from app.modules.orders.application.dto.commands import ConfirmOrderCommand
from app.modules.orders.domain.exceptions import OrderNotFoundException
from app.modules.orders.domain.repositories.order_repository import OrderRepository
from app.modules.orders.domain.value_objects.order_id import OrderId


class ConfirmOrderUseCase:
    """Use case for confirming an order.

    This use case handles the business flow of confirming an order.
    """

    def __init__(self, order_repository: OrderRepository) -> None:
        """Initialize use case.

        Args:
            order_repository: Order repository
        """
        self.order_repository = order_repository

    def execute(self, command: ConfirmOrderCommand) -> None:
        """Execute the use case.

        Args:
            command: Confirm order command

        Raises:
            OrderNotFoundException: If order not found
        """
        # Find order
        order_id = OrderId(UUID(command.order_id))
        order = self.order_repository.find_by_id(order_id)

        if not order:
            raise OrderNotFoundException(command.order_id)

        # Execute business logic
        order.confirm()

        # Persist changes
        self.order_repository.save(order)
