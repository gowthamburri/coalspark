"""
app/models/restaurant.py
Restaurant profile — one record stores CoalSpark's details.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Boolean, CheckConstraint, Index
from sqlalchemy.orm import relationship
from app.db.session import Base


class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    tagline = Column(String(300), nullable=True)
    description = Column(Text, nullable=True)
    address = Column(String(500), nullable=False)
    city = Column(String(100), nullable=False, default="Hyderabad")
    phone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    rating = Column(Float, default=4.5)
    total_reviews = Column(Integer, default=0)
    opening_time = Column(String(10), default="11:00")
    closing_time = Column(String(10), default="23:00")
    logo_url = Column(String(500), nullable=True)
    banner_url = Column(String(500), nullable=True)
    cuisine_types = Column(String(300), default="BBQ, Biryani, Mandi, Chinese, Italian")
    is_open = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    menu_items = relationship("MenuItem", back_populates="restaurant", cascade="all, delete-orphan")
    coupons = relationship("Coupon", back_populates="restaurant", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="restaurant", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint("rating >= 0 AND rating <= 5", name="ck_restaurants_rating_range"),
        CheckConstraint("total_reviews >= 0", name="ck_restaurants_total_reviews_non_negative"),
        Index("ix_restaurants_city_is_open", "city", "is_open"),
    )

    def __repr__(self):
        return f"<Restaurant {self.name}>"