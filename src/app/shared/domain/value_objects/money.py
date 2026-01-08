"""Money value object."""

from dataclasses import dataclass
from decimal import Decimal


class CurrencyMismatchError(ValueError):
    """Raised when operations are performed on Money with different currencies."""

    pass


@dataclass(frozen=True)
class Money:
    """Represents a monetary amount with currency.

    This is an immutable value object that ensures currency consistency
    in all operations.

    Attributes:
        amount: The monetary amount
        currency: ISO 4217 currency code (default: JPY)

    Example:
        >>> price = Money(Decimal("1000"), "JPY")
        >>> tax = Money(Decimal("100"), "JPY")
        >>> total = price.add(tax)
        >>> print(total.amount)
        1100
    """

    amount: Decimal
    currency: str = "JPY"

    def __post_init__(self) -> None:
        """Validate money attributes."""
        if not isinstance(self.amount, Decimal):
            object.__setattr__(self, "amount", Decimal(str(self.amount)))

    def add(self, other: "Money") -> "Money":
        """Add two Money objects.

        Args:
            other: Money to add

        Returns:
            New Money object with the sum

        Raises:
            CurrencyMismatchError: If currencies don't match
        """
        self._check_currency(other)
        return Money(self.amount + other.amount, self.currency)

    def subtract(self, other: "Money") -> "Money":
        """Subtract two Money objects.

        Args:
            other: Money to subtract

        Returns:
            New Money object with the difference

        Raises:
            CurrencyMismatchError: If currencies don't match
        """
        self._check_currency(other)
        return Money(self.amount - other.amount, self.currency)

    def multiply(self, multiplier: Decimal | int | float) -> "Money":
        """Multiply Money by a number.

        Args:
            multiplier: Number to multiply by

        Returns:
            New Money object with the product
        """
        if not isinstance(multiplier, Decimal):
            multiplier = Decimal(str(multiplier))
        return Money(self.amount * multiplier, self.currency)

    def divide(self, divisor: Decimal | int | float) -> "Money":
        """Divide Money by a number.

        Args:
            divisor: Number to divide by

        Returns:
            New Money object with the quotient

        Raises:
            ZeroDivisionError: If divisor is zero
        """
        if not isinstance(divisor, Decimal):
            divisor = Decimal(str(divisor))
        return Money(self.amount / divisor, self.currency)

    def is_zero(self) -> bool:
        """Check if amount is zero.

        Returns:
            True if amount is zero
        """
        return self.amount == Decimal("0")

    def is_positive(self) -> bool:
        """Check if amount is positive.

        Returns:
            True if amount is greater than zero
        """
        return self.amount > Decimal("0")

    def is_negative(self) -> bool:
        """Check if amount is negative.

        Returns:
            True if amount is less than zero
        """
        return self.amount < Decimal("0")

    def _check_currency(self, other: "Money") -> None:
        """Verify that two Money objects have the same currency.

        Args:
            other: Money to compare with

        Raises:
            CurrencyMismatchError: If currencies don't match
        """
        if self.currency != other.currency:
            raise CurrencyMismatchError(
                f"Cannot operate on different currencies: {self.currency} and {other.currency}"
            )

    def __str__(self) -> str:
        """String representation."""
        return f"{self.amount} {self.currency}"

    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return f"Money(amount={self.amount}, currency='{self.currency}')"
