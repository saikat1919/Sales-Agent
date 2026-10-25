from typing import Annotated
from fastapi import APIRouter, Query, status
from app.modules.catalog.dependencies import ProductServiceDep
from app.modules.catalog.schemas import ProductCreate, ProductRead, Page, ProductFilters, ProductUpdate

router = APIRouter(prefix="/products", tags=["products"])


@router.get(path="", response_model=Page)
async def list_products(
        filters: Annotated[ProductFilters, Query()],
        service: ProductServiceDep
) -> Page:
    return await service.get_all_products(filters)

@router.get(path="/{slug}", response_model=ProductRead)
async def get_product(slug: str, service: ProductServiceDep) -> ProductRead:
    return await service.get_product(slug)

@router.post(path="", response_model=ProductRead)
async def create_product(data: ProductCreate, service: ProductServiceDep) -> ProductRead:
    return await service.create_product(data)

@router.patch(path="/{slug}", response_model=ProductRead)
async def update_product(slug: str, data: ProductUpdate, service: ProductServiceDep) -> ProductRead:
    return await service.update_product(slug, data)

@router.delete(path="/{slug}", status_code=status.HTTP_204_NO_CONTENT)
async def archive_product(slug: str, service: ProductServiceDep) -> None:
    await service.archive_product(slug)