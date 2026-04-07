"""
app/schemas/menu_item.py
Pydantic schemas for menu CRUD operations.
"""
from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime
from app.models.menu_item import MenuCategory


class MenuItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category: MenuCategory
    is_vegetarian: bool = False
    is_available: bool = True
    is_featured: bool = False
    spice_level: int = 2
    preparation_time: int = 20

    @field_validator("price")
    @classmethod
    def price_positive(cls, v):
        if v <= 0:
            raise ValueError("Price must be greater than 0")
        return round(v, 2)

    @field_validator("spice_level")
    @classmethod
    def spice_range(cls, v):
        if not 1 <= v <= 5:
            raise ValueError("Spice level must be between 1 and 5")
        return v


class MenuItemCreate(MenuItemBase):
    restaurant_id: int


class MenuItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[MenuCategory] = None
    is_vegetarian: Optional[bool] = None
    is_available: Optional[bool] = None
    is_featured: Optional[bool] = None
    spice_level: Optional[int] = None
    preparation_time: Optional[int] = None
    image_url: Optional[str] = None


class MenuItemRead(MenuItemBase):
    id: int
    restaurant_id: int
    image_url: Optional[str] = None
    avg_rating: float = 0.0
    reviews_count: int = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True