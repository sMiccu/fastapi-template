"""OrderId value object."""

from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass(frozen=True)
class OrderId:
    """Order identifier value object."""

    value: UUID

    @classmethod
    def generate(cls) -> "OrderId":
        """Generate a new OrderId.

        Returns:
            New OrderId instance
        """
        return cls(uuid4())

    def __str__(self) -> str:
        """String representation."""
        return str(self.value)

    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return f"OrderId({self.value!r})"
