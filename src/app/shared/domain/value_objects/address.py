"""Address value object."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Address:
    """Represents a postal address.

    This is an immutable value object for address information.

    Attributes:
        postal_code: Postal code
        prefecture: Prefecture/State
        city: City
        street: Street address
        building: Building name/apartment number (optional)

    Example:
        >>> address = Address(
        ...     postal_code="123-4567",
        ...     prefecture="Tokyo",
        ...     city="Shibuya-ku",
        ...     street="1-2-3 Dogenzaka",
        ...     building="ABC Building 4F"
        ... )
        >>> print(address.full_address())
        123-4567 Tokyo Shibuya-ku 1-2-3 Dogenzaka ABC Building 4F
    """

    postal_code: str
    prefecture: str
    city: str
    street: str
    building: str | None = None

    def full_address(self) -> str:
        """Get full address as a single string.

        Returns:
            Complete address string
        """
        parts = [self.postal_code, self.prefecture, self.city, self.street]
        if self.building:
            parts.append(self.building)
        return " ".join(parts)

    def __str__(self) -> str:
        """String representation."""
        return self.full_address()

    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return (
            f"Address(postal_code='{self.postal_code}', "
            f"prefecture='{self.prefecture}', "
            f"city='{self.city}', "
            f"street='{self.street}', "
            f"building={self.building!r})"
        )
