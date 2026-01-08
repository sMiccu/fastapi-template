"""API router for catalog module."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.modules.catalog.dependencies import get_product_service
from app.modules.catalog.exceptions import ProductNotFoundException
from app.modules.catalog.schemas import (
    ProductCreate,
    ProductResponse,
    ProductUpdate,
)
from app.modules.catalog.service import ProductService

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=list[ProductResponse])
def list_products(
    service: Annotated[ProductService, Depends(get_product_service)],
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
) -> list[ProductResponse]:
    """List all products.

    Args:
        skip: Number of products to skip
        limit: Maximum number of products to return
        service: Product service (injected)

    Returns:
        List of products
    """
    products = service.list_products(skip, limit)
    return [ProductResponse.model_validate(p) for p in products]


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: UUID,
    service: Annotated[ProductService, Depends(get_product_service)],
) -> ProductResponse:
    """Get a product by ID.

    Args:
        product_id: Product UUID
        service: Product service (injected)

    Returns:
        Product details

    Raises:
        HTTPException: If product not found
    """
    try:
        product = service.get_product(product_id)
        return ProductResponse.model_validate(product)
    except ProductNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    product_data: ProductCreate,
    service: Annotated[ProductService, Depends(get_product_service)],
) -> ProductResponse:
    """Create a new product.

    Args:
        product_data: Product creation data
        service: Product service (injected)

    Returns:
        Created product
    """
    product = service.create_product(product_data)
    return ProductResponse.model_validate(product)


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: UUID,
    product_data: ProductUpdate,
    service: Annotated[ProductService, Depends(get_product_service)],
) -> ProductResponse:
    """Update a product.

    Args:
        product_id: Product UUID
        product_data: Product update data
        service: Product service (injected)

    Returns:
        Updated product

    Raises:
        HTTPException: If product not found
    """
    try:
        product = service.update_product(product_id, product_data)
        return ProductResponse.model_validate(product)
    except ProductNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: UUID,
    service: Annotated[ProductService, Depends(get_product_service)],
) -> None:
    """Delete a product.

    Args:
        product_id: Product UUID
        service: Product service (injected)

    Raises:
        HTTPException: If product not found
    """
    try:
        service.delete_product(product_id)
    except ProductNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


@router.get("/{product_id}/availability", response_model=dict)
def check_availability(
    product_id: UUID,
    service: Annotated[ProductService, Depends(get_product_service)],
) -> dict[str, str | bool]:
    """Check if a product is available.

    Args:
        product_id: Product UUID
        service: Product service (injected)

    Returns:
        Availability status

    Raises:
        HTTPException: If product not found
    """
    try:
        is_available = service.is_available(product_id)
        return {"product_id": str(product_id), "is_available": is_available}
    except ProductNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
