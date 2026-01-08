"""Unit tests for Order entity."""

from decimal import Decimal
from uuid import uuid4

import pytest
from app.modules.orders.domain.entities.order import Order
from app.modules.orders.domain.exceptions import (
    EmptyOrderError,
    InvalidQuantityError,
    OrderAlreadyConfirmedError,
)
from app.modules.orders.domain.value_objects.customer_id import CustomerId
from app.modules.orders.domain.value_objects.order_status import OrderStatus
from app.modules.orders.domain.value_objects.product_id import ProductId
from app.shared.domain.value_objects.money import Money


@pytest.mark.unit
class TestOrder:
    """Tests for Order entity."""

    @pytest.fixture
    def customer_id(self) -> CustomerId:
        """Create a customer ID for tests."""
        return CustomerId(uuid4())

    @pytest.fixture
    def product_id(self) -> ProductId:
        """Create a product ID for tests."""
        return ProductId(uuid4())

    def test_create_order(self, customer_id: CustomerId):
        """Test creating an order."""
        order = Order.create(customer_id)
        assert order.customer_id == customer_id
        assert order.status == OrderStatus.PENDING
        assert len(order.items) == 0

    def test_add_item_to_order(self, customer_id: CustomerId, product_id: ProductId):
        """Test adding an item to an order."""
        order = Order.create(customer_id)
        order.add_item(product_id, 2, Money(Decimal("1000"), "JPY"))

        assert len(order.items) == 1
        assert order.items[0].quantity == 2
        assert order.items[0].unit_price == Money(Decimal("1000"), "JPY")

    def test_add_item_with_invalid_quantity_raises_error(
        self, customer_id: CustomerId, product_id: ProductId
    ):
        """Test adding item with invalid quantity raises error."""
        order = Order.create(customer_id)

        with pytest.raises(InvalidQuantityError):
            order.add_item(product_id, 0, Money(Decimal("1000"), "JPY"))

    def test_add_item_to_confirmed_order_raises_error(
        self, customer_id: CustomerId, product_id: ProductId
    ):
        """Test adding item to confirmed order raises error."""
        order = Order.create(customer_id)
        order.add_item(product_id, 1, Money(Decimal("1000"), "JPY"))
        order.confirm()

        with pytest.raises(OrderAlreadyConfirmedError):
            order.add_item(product_id, 1, Money(Decimal("1000"), "JPY"))

    def test_calculate_total(self, customer_id: CustomerId):
        """Test calculating order total."""
        order = Order.create(customer_id)
        order.add_item(ProductId(uuid4()), 2, Money(Decimal("1000"), "JPY"))
        order.add_item(ProductId(uuid4()), 1, Money(Decimal("500"), "JPY"))

        total = order.calculate_total()
        assert total == Money(Decimal("2500"), "JPY")

    def test_confirm_order_success(self, customer_id: CustomerId, product_id: ProductId):
        """Test confirming an order successfully."""
        order = Order.create(customer_id)
        order.add_item(product_id, 1, Money(Decimal("1000"), "JPY"))
        order.confirm()

        assert order.status == OrderStatus.CONFIRMED

    def test_confirm_empty_order_raises_error(self, customer_id: CustomerId):
        """Test confirming empty order raises error."""
        order = Order.create(customer_id)

        with pytest.raises(EmptyOrderError):
            order.confirm()

    def test_cancel_order(self, customer_id: CustomerId, product_id: ProductId):
        """Test cancelling an order."""
        order = Order.create(customer_id)
        order.add_item(product_id, 1, Money(Decimal("1000"), "JPY"))
        order.cancel()

        assert order.status == OrderStatus.CANCELLED
