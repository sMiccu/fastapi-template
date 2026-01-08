"""Dependencies for orders API."""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.orders.application.use_cases.add_item_to_order import (
    AddItemToOrderUseCase,
)
from app.modules.orders.application.use_cases.confirm_order import ConfirmOrderUseCase
from app.modules.orders.application.use_cases.create_order import CreateOrderUseCase
from app.modules.orders.application.use_cases.get_order import GetOrderUseCase
from app.modules.orders.domain.repositories.order_repository import OrderRepository
from app.modules.orders.infrastructure.persistence.order_repository_impl import (
    OrderRepositoryImpl,
)


def get_order_repository(session: Annotated[Session, Depends(get_db)]) -> OrderRepository:
    """Get order repository instance.

    Args:
        session: Database session

    Returns:
        Order repository implementation
    """
    return OrderRepositoryImpl(session)


def get_create_order_use_case(
    repository: Annotated[OrderRepository, Depends(get_order_repository)],
) -> CreateOrderUseCase:
    """Get create order use case.

    Args:
        repository: Order repository

    Returns:
        Create order use case
    """
    return CreateOrderUseCase(repository)


def get_add_item_use_case(
    repository: Annotated[OrderRepository, Depends(get_order_repository)],
) -> AddItemToOrderUseCase:
    """Get add item to order use case.

    Args:
        repository: Order repository

    Returns:
        Add item use case
    """
    return AddItemToOrderUseCase(repository)


def get_confirm_order_use_case(
    repository: Annotated[OrderRepository, Depends(get_order_repository)],
) -> ConfirmOrderUseCase:
    """Get confirm order use case.

    Args:
        repository: Order repository

    Returns:
        Confirm order use case
    """
    return ConfirmOrderUseCase(repository)


def get_get_order_use_case(
    repository: Annotated[OrderRepository, Depends(get_order_repository)],
) -> GetOrderUseCase:
    """Get order use case.

    Args:
        repository: Order repository

    Returns:
        Get order use case
    """
    return GetOrderUseCase(repository)
