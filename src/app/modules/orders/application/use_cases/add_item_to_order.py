"""Add item to order use case."""

from uuid import UUID

from app.modules.orders.application.dto.commands import AddItemToOrderCommand
from app.modules.orders.domain.exceptions import OrderNotFoundException
from app.modules.orders.domain.repositories.order_repository import OrderRepository
from app.modules.orders.domain.value_objects.order_id import OrderId
from app.modules.orders.domain.value_objects.product_id import ProductId
from app.shared.domain.value_objects.money import Money


class AddItemToOrderUseCase:
    """Use case for adding an item to an order.

    This use case handles the business flow of adding items to an existing order.
    """

    def __init__(self, order_repository: OrderRepository) -> None:
        """Initialize use case.

        Args:
            order_repository: Order repository
        """
        self.order_repository = order_repository

    def execute(self, command: AddItemToOrderCommand) -> None:
        """Execute the use case.

        Args:
            command: Add item command

        Raises:
            OrderNotFoundException: If order not found
        """
        # Find order
        order_id = OrderId(UUID(command.order_id))
        order = self.order_repository.find_by_id(order_id)

        if not order:
            raise OrderNotFoundException(command.order_id)

        # Convert DTOs to domain objects
        product_id = ProductId(UUID(command.product_id))
        unit_price = Money(command.unit_price, command.currency)

        # Execute business logic (in domain entity)
        order.add_item(product_id, command.quantity, unit_price)

        # Persist changes
        self.order_repository.save(order)
