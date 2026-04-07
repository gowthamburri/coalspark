"""
app/schemas/order.py
Pydantic schemas for order creation and retrieval.
"""
from pydantic import BaseModel, field_validator
from typing import List, Optional
from datetime import datetime
from app.models.order import OrderStatus
from app.schemas.menu_item import MenuItemRead


# ── Order Item schemas ───────────────────────────────────────────────────────
class OrderItemCreate(BaseModel):
    menu_item_id: int
    quantity: int

    @field_validator("quantity")
    @classmethod
    def quantity_positive(cls, v):
        if v <= 0:
            raise ValueError("Quantity must be at least 1")
        if v > 20:
            raise ValueError("Maximum 20 items per menu item")
        return v


class OrderItemRead(BaseModel):
    id: int
    menu_item_id: Optional[int]
    quantity: int
    unit_price: float
    subtotal: float
    menu_item: Optional[MenuItemRead] = None

    class Config:
        from_attributes = True


# ── Order schemas ────────────────────────────────────────────────────────────
class OrderCreate(BaseModel):
    items: List[OrderItemCreate]
    delivery_address: Optional[str] = None
    special_instructions: Optional[str] = None
    payment_method: str = "cash"
    coupon_code: Optional[str] = None

    @field_validator("items")
    @classmethod
    def items_not_empty(cls, v):
        if not v:
            raise ValueError("Order must have at least one item")
        return v


class OrderStatusUpdate(BaseModel):
    status: OrderStatus


class OrderRead(BaseModel):
    id: int
    user_id: int
    status: OrderStatus
    total_amount: float
    delivery_address: Optional[str]
    special_instructions: Optional[str]
    payment_method: str
    is_paid: bool
    order_items: List[OrderItemRead] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True