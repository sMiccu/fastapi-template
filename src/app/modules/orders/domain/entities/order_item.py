"""OrderItem entity."""

from dataclasses import dataclass

from app.modules.orders.domain.exceptions import InvalidQuantityError
from app.modules.orders.domain.value_objects.product_id import ProductId
from app.shared.domain.value_objects.money import Money


@dataclass
class OrderItem:
    """Order item entity.

    Represents a single line item in an order.

    Attributes:
        product_id: Product identifier
        quantity: Quantity ordered
        unit_price: Price per unit
    """

    product_id: ProductId
    quantity: int
    unit_price: Money

    def __post_init__(self) -> None:
        """Validate order item."""
        if self.quantity <= 0:
            raise InvalidQuantityError(self.quantity)

    def subtotal(self) -> Money:
        """Calculate subtotal for this item.

        Returns:
            Subtotal amount
        """
        return self.unit_price.multiply(self.quantity)

    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return (
            f"OrderItem(product_id={self.product_id!r}, "
            f"quantity={self.quantity}, "
            f"unit_price={self.unit_price!r})"
        )
