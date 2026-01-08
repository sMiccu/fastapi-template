"""Request schemas for orders API."""

from decimal import Decimal

from pydantic import BaseModel, Field


class CreateOrderRequest(BaseModel):
    """Request schema for creating an order."""

    customer_id: str = Field(..., description="Customer UUID")


class AddItemRequest(BaseModel):
    """Request schema for adding an item to an order."""

    product_id: str = Field(..., description="Product UUID")
    quantity: int = Field(..., gt=0, description="Quantity (must be positive)")
    unit_price: Decimal = Field(..., gt=0, description="Unit price")
    currency: str = Field(default="JPY", pattern="^[A-Z]{3}$", description="Currency code")
