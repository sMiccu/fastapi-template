"""Domain exceptions for orders module."""

from app.shared.exceptions import BusinessRuleViolation, NotFoundException


class OrderException(BusinessRuleViolation):
    """Base exception for order domain."""

    pass


class OrderNotFoundException(NotFoundException):
    """Raised when an order is not found."""

    def __init__(self, order_id: str) -> None:
        super().__init__(f"Order not found: {order_id}")


class EmptyOrderError(OrderException):
    """Raised when trying to confirm an order without items."""

    def __init__(self) -> None:
        super().__init__("Cannot confirm an empty order")


class OrderAlreadyConfirmedError(OrderException):
    """Raised when trying to modify a confirmed order."""

    def __init__(self) -> None:
        super().__init__("Cannot modify a confirmed order")


class OrderCannotBeCancelledError(OrderException):
    """Raised when trying to cancel an order that cannot be cancelled."""

    def __init__(self, status: str) -> None:
        super().__init__(f"Cannot cancel order with status: {status}")


class InvalidQuantityError(OrderException):
    """Raised when quantity is invalid."""

    def __init__(self, quantity: int) -> None:
        super().__init__(f"Invalid quantity: {quantity}")
