"""Main API v1 router that combines all module routers."""

from fastapi import APIRouter

from app.modules.catalog.router import router as catalog_router
from app.modules.orders.presentation.api.router import router as orders_router

api_router = APIRouter(prefix="/api/v1")

# Include module routers
api_router.include_router(catalog_router)
api_router.include_router(orders_router)
