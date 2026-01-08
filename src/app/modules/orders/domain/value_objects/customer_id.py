"""CustomerId value object."""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class CustomerId:
    """Customer identifier value object."""

    value: UUID

    def __str__(self) -> str:
        """String representation."""
        return str(self.value)

    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return f"CustomerId({self.value!r})"
