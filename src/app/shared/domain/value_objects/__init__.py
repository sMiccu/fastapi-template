"""Shared value objects used across bounded contexts."""

from app.shared.domain.value_objects.address import Address
from app.shared.domain.value_objects.email import Email
from app.shared.domain.value_objects.money import Money

__all__ = ["Money", "Email", "Address"]
