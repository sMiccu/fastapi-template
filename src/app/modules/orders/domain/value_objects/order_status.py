"""OrderStatus value object."""

from enum import Enum


class OrderStatus(str, Enum):
    """Order status enumeration."""

    PENDING = "pending"
    CONFIRMED = "confirmed"
    PAID = "paid"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

    def __str__(self) -> str:
        """String representation."""
        return self.value
