"""Email value object."""

import re
from dataclasses import dataclass


class InvalidEmailError(ValueError):
    """Raised when email format is invalid."""

    pass


@dataclass(frozen=True)
class Email:
    """Represents an email address.

    This is an immutable value object that validates email format.

    Attributes:
        value: The email address string

    Example:
        >>> email = Email("user@example.com")
        >>> print(email.value)
        user@example.com

        >>> invalid = Email("invalid-email")  # Raises InvalidEmailError
    """

    value: str

    def __post_init__(self) -> None:
        """Validate email format."""
        if not self._is_valid(self.value):
            raise InvalidEmailError(f"Invalid email format: {self.value}")

    @staticmethod
    def _is_valid(email: str) -> bool:
        """Check if email format is valid.

        Args:
            email: Email string to validate

        Returns:
            True if valid, False otherwise
        """
        # Basic email validation pattern
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))

    def domain(self) -> str:
        """Extract domain from email.

        Returns:
            Domain part of the email
        """
        return self.value.split("@")[1]

    def local_part(self) -> str:
        """Extract local part from email.

        Returns:
            Local part of the email (before @)
        """
        return self.value.split("@")[0]

    def __str__(self) -> str:
        """String representation."""
        return self.value

    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return f"Email('{self.value}')"
