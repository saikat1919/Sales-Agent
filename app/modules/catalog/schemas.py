from decimal import Decimal
from typing import Any
import uuid
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict
from app.modules.catalog.models import Category


class ProductBase(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    brand: str = Field(min_length=2, max_length=255)
    category: Category
    price: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    stock: int = Field(ge=0)
    warranty: int = Field(ge=0, default=12)
    description: str = ""
    specs: dict[str, Any] = {}

class ProductCreate(ProductBase):
    slug: str = Field(min_length=2, max_length=255)

class ProductRead(ProductBase):
    id: uuid.UUID
    slug: str
    in_stock: bool

    model_config = ConfigDict(from_attributes=True)

class ProductUpdate(BaseModel):
    """Every Field is optional: Only what the client sends is changed"""
    name: str | None = Field(default=None, min_length=2, max_length=255)
    price: Decimal | None = Field(default=None, gt=0, max_digits=10, decimal_places=2)
    stock: int | None = Field(default=None, ge=0)
    warranty: int | None = Field(ge=0, default=None)
    description: str | None = None
    specs: dict[str, Any] | None = None


class SortOption(str, Enum):
    NEWEST = "newest"
    PRICE_ASC = "price_asc"
    PRICE_DESC = "price_desc"
    NAME = "name"

class ProductFilters(BaseModel):
    """Query Parameters for filtering products"""
    q: str | None = Field(default=None, min_length=2, max_length=100)
    category: Category | None = None
    brand: str | None = None
    min_price: Decimal | None = Field(gt=0, default=None)
    max_price: Decimal | None = Field(gt=0, default=None)
    in_stock: bool | None = None
    sort: SortOption = SortOption.NEWEST
    page: int = 1
    page_size: int = 10

class Page(BaseModel):
    items: list[ProductRead]
    total: int
    page: int
    page_size: int