"""Shared exception hierarchy for the application."""


class AppException(Exception):
    """Base exception for all application exceptions."""

    def __init__(self, message: str = "") -> None:
        self.message = message
        super().__init__(self.message)


class DomainException(AppException):
    """Base exception for domain layer."""

    pass


class InfrastructureException(AppException):
    """Base exception for infrastructure layer."""

    pass


class NotFoundException(AppException):
    """Exception raised when a resource is not found."""

    pass


class ValidationException(AppException):
    """Exception raised when validation fails."""

    pass


class BusinessRuleViolation(DomainException):
    """Exception raised when a business rule is violated."""

    pass
