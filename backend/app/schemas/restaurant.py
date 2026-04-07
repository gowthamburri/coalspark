"""
app/schemas/restaurant.py
Pydantic schemas for restaurant profile.
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class RestaurantRead(BaseModel):
    id: int
    name: str
    tagline: Optional[str]
    description: Optional[str]
    address: str
    city: str
    phone: Optional[str]
    email: Optional[str]
    rating: float
    total_reviews: int
    opening_time: str
    closing_time: str
    logo_url: Optional[str]
    banner_url: Optional[str]
    cuisine_types: str
    is_open: str

    class Config:
        from_attributes = True


class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    tagline: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    opening_time: Optional[str] = None
    closing_time: Optional[str] = None
    is_open: Optional[str] = None