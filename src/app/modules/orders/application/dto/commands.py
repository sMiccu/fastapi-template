"""Command DTOs for orders use cases."""

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class CreateOrderCommand:
    """Command to create a new order."""

    customer_id: str


@dataclass(frozen=True)
class AddItemToOrderCommand:
    """Command to add an item to an order."""

    order_id: str
    product_id: str
    quantity: int
    unit_price: Decimal
    currency: str = "JPY"


@dataclass(frozen=True)
class ConfirmOrderCommand:
    """Command to confirm an order."""

    order_id: str
