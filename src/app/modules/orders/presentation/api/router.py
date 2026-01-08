"""API router for orders."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.modules.orders.application.dto.commands import (
    AddItemToOrderCommand,
    ConfirmOrderCommand,
    CreateOrderCommand,
)
from app.modules.orders.application.use_cases.add_item_to_order import (
    AddItemToOrderUseCase,
)
from app.modules.orders.application.use_cases.confirm_order import ConfirmOrderUseCase
from app.modules.orders.application.use_cases.create_order import CreateOrderUseCase
from app.modules.orders.application.use_cases.get_order import GetOrderUseCase
from app.modules.orders.domain.exceptions import OrderException, OrderNotFoundException
from app.modules.orders.presentation.api.dependencies import (
    get_add_item_use_case,
    get_confirm_order_use_case,
    get_create_order_use_case,
    get_get_order_use_case,
)
from app.modules.orders.presentation.schemas.request import (
    AddItemRequest,
    CreateOrderRequest,
)
from app.modules.orders.presentation.schemas.response import (
    OrderItemResponse,
    OrderResponse,
)

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_order(
    request: CreateOrderRequest,
    use_case: Annotated[CreateOrderUseCase, Depends(get_create_order_use_case)],
) -> dict[str, str]:
    """Create a new order.

    Args:
        request: Order creation request
        use_case: Create order use case (injected)

    Returns:
        Created order ID
    """
    command = CreateOrderCommand(customer_id=request.customer_id)
    order_id = use_case.execute(command)
    return {"order_id": str(order_id.value)}


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: str,
    use_case: Annotated[GetOrderUseCase, Depends(get_get_order_use_case)],
) -> OrderResponse:
    """Get an order by ID.

    Args:
        order_id: Order UUID
        use_case: Get order use case (injected)

    Returns:
        Order details

    Raises:
        HTTPException: If order not found
    """
    try:
        order = use_case.execute(order_id)

        # Convert domain entity to response DTO
        total = order.calculate_total()
        items = [
            OrderItemResponse(
                product_id=str(item.product_id.value),
                quantity=item.quantity,
                unit_price=item.unit_price.amount,
                currency=item.unit_price.currency,
                subtotal=item.subtotal().amount,
            )
            for item in order.items
        ]

        return OrderResponse(
            id=str(order.id.value),
            customer_id=str(order.customer_id.value),
            status=order.status.value,
            items=items,
            total=total.amount,
            currency=total.currency,
            created_at=order.created_at,
        )
    except OrderNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


@router.post("/{order_id}/items", status_code=status.HTTP_204_NO_CONTENT)
def add_item_to_order(
    order_id: str,
    request: AddItemRequest,
    use_case: Annotated[AddItemToOrderUseCase, Depends(get_add_item_use_case)],
) -> None:
    """Add an item to an order.

    Args:
        order_id: Order UUID
        request: Add item request
        use_case: Add item use case (injected)

    Raises:
        HTTPException: If order not found or business rule violated
    """
    try:
        command = AddItemToOrderCommand(
            order_id=order_id,
            product_id=request.product_id,
            quantity=request.quantity,
            unit_price=request.unit_price,
            currency=request.currency,
        )
        use_case.execute(command)
    except OrderNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except OrderException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e


@router.post("/{order_id}/confirm", status_code=status.HTTP_204_NO_CONTENT)
def confirm_order(
    order_id: str,
    use_case: Annotated[ConfirmOrderUseCase, Depends(get_confirm_order_use_case)],
) -> None:
    """Confirm an order.

    Args:
        order_id: Order UUID
        use_case: Confirm order use case (injected)

    Raises:
        HTTPException: If order not found or business rule violated
    """
    try:
        command = ConfirmOrderCommand(order_id=order_id)
        use_case.execute(command)
    except OrderNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except OrderException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
