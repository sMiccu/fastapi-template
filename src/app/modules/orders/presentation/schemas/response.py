"""Response schemas for orders API."""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class OrderItemResponse(BaseModel):
    """Response schema for order item."""

    product_id: str
    quantity: int
    unit_price: Decimal
    currency: str
    subtotal: Decimal


class OrderResponse(BaseModel):
    """Response schema for order."""

    id: str = Field(..., description="Order UUID")
    customer_id: str = Field(..., description="Customer UUID")
    status: str = Field(..., description="Order status")
    items: list[OrderItemResponse] = Field(default_factory=list, description="Order items")
    total: Decimal = Field(..., description="Total amount")
    currency: str = Field(..., description="Currency code")
    created_at: datetime = Field(..., description="Creation timestamp")
