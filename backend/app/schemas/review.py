from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_validator


class ReviewCreate(BaseModel):
    order_id: int
    menu_item_id: int
    rating: int
    title: Optional[str] = None
    comment: Optional[str] = None

    @field_validator("rating")
    @classmethod
    def validate_rating(cls, value: int) -> int:
        if value < 1 or value > 5:
            raise ValueError("Rating must be between 1 and 5")
        return value


class ReviewRead(BaseModel):
    id: int
    user_id: int
    restaurant_id: int
    menu_item_id: int
    order_id: int
    rating: int
    title: Optional[str]
    comment: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

