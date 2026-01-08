"""Unit tests for Money value object."""

from decimal import Decimal

import pytest
from app.shared.domain.value_objects.money import CurrencyMismatchError, Money


@pytest.mark.unit
class TestMoney:
    """Tests for Money value object."""

    def test_create_money(self):
        """Test creating a Money object."""
        money = Money(Decimal("1000"), "JPY")
        assert money.amount == Decimal("1000")
        assert money.currency == "JPY"

    def test_add_same_currency(self):
        """Test adding money with same currency."""
        money1 = Money(Decimal("1000"), "JPY")
        money2 = Money(Decimal("500"), "JPY")
        result = money1.add(money2)
        assert result.amount == Decimal("1500")
        assert result.currency == "JPY"

    def test_add_different_currency_raises_error(self):
        """Test adding money with different currency raises error."""
        money1 = Money(Decimal("1000"), "JPY")
        money2 = Money(Decimal("500"), "USD")
        with pytest.raises(CurrencyMismatchError):
            money1.add(money2)

    def test_subtract(self):
        """Test subtracting money."""
        money1 = Money(Decimal("1000"), "JPY")
        money2 = Money(Decimal("300"), "JPY")
        result = money1.subtract(money2)
        assert result.amount == Decimal("700")

    def test_multiply(self):
        """Test multiplying money."""
        money = Money(Decimal("100"), "JPY")
        result = money.multiply(3)
        assert result.amount == Decimal("300")

    def test_is_zero(self):
        """Test checking if money is zero."""
        zero = Money(Decimal("0"), "JPY")
        non_zero = Money(Decimal("100"), "JPY")
        assert zero.is_zero()
        assert not non_zero.is_zero()

    def test_is_positive(self):
        """Test checking if money is positive."""
        positive = Money(Decimal("100"), "JPY")
        negative = Money(Decimal("-100"), "JPY")
        assert positive.is_positive()
        assert not negative.is_positive()
