"""Value objects for orders domain."""

from app.modules.orders.domain.value_objects.customer_id import CustomerId
from app.modules.orders.domain.value_objects.order_id import OrderId
from app.modules.orders.domain.value_objects.order_status import OrderStatus
from app.modules.orders.domain.value_objects.product_id import ProductId

__all__ = ["OrderId", "CustomerId", "ProductId", "OrderStatus"]
