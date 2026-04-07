from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_validator

from app.models.coupon import CouponType


class CouponCreate(BaseModel):
    restaurant_id: int
    code: str
    discount_type: CouponType
    discount_value: float
    min_order_amount: float = 0
    max_discount_amount: Optional[float] = None
    usage_limit: Optional[int] = None
    starts_at: datetime
    expires_at: datetime
    is_active: bool = True

    @field_validator("code")
    @classmethod
    def normalize_code(cls, value: str) -> str:
        code = value.strip().upper()
        if not code:
            raise ValueError("Coupon code cannot be empty")
        return code


class CouponUpdate(BaseModel):
    discount_value: Optional[float] = None
    min_order_amount: Optional[float] = None
    max_discount_amount: Optional[float] = None
    usage_limit: Optional[int] = None
    starts_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    is_active: Optional[bool] = None


class CouponRead(BaseModel):
    id: int
    restaurant_id: int
    code: str
    discount_type: CouponType
    discount_value: float
    min_order_amount: float
    max_discount_amount: Optional[float]
    usage_limit: Optional[int]
    used_count: int
    starts_at: datetime
    expires_at: datetime
    is_active: bool

    class Config:
        from_attributes = True


class CouponValidateRequest(BaseModel):
    code: str
    subtotal: float

    @field_validator("code")
    @classmethod
    def normalize_code(cls, value: str) -> str:
        return value.strip().upper()


class CouponValidateResponse(BaseModel):
    code: str
    is_valid: bool
    message: str
    discount_amount: float
    final_total: float

