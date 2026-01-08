"""Pydantic schemas for catalog module."""

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field


# Product schemas
class ProductBase(BaseModel):
    """Base product schema."""

    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    price: Decimal = Field(..., gt=0)
    currency: str = Field(default="JPY", pattern="^[A-Z]{3}$")
    category_id: UUID | None = None
    stock_quantity: int = Field(default=0, ge=0)
    is_active: bool = True


class ProductCreate(ProductBase):
    """Schema for creating a product."""

    pass


class ProductUpdate(BaseModel):
    """Schema for updating a product."""

    name: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None
    price: Decimal | None = Field(None, gt=0)
    currency: str | None = Field(None, pattern="^[A-Z]{3}$")
    category_id: UUID | None = None
    stock_quantity: int | None = Field(None, ge=0)
    is_active: bool | None = None


class ProductResponse(ProductBase):
    """Schema for product response."""

    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# Category schemas
class CategoryBase(BaseModel):
    """Base category schema."""

    name: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=255, pattern="^[a-z0-9-]+$")
    parent_id: UUID | None = None


class CategoryCreate(CategoryBase):
    """Schema for creating a category."""

    pass


class CategoryUpdate(BaseModel):
    """Schema for updating a category."""

    name: str | None = Field(None, min_length=1, max_length=255)
    slug: str | None = Field(None, min_length=1, max_length=255, pattern="^[a-z0-9-]+$")
    parent_id: UUID | None = None


class CategoryResponse(CategoryBase):
    """Schema for category response."""

    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
