"""
app/models/review.py
Reviews linked to delivered orders and menu items.
"""
from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    CheckConstraint,
    Index,
)
from sqlalchemy.orm import relationship

from app.db.session import Base


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id", ondelete="CASCADE"), nullable=False)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id", ondelete="CASCADE"), nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    rating = Column(Integer, nullable=False)
    title = Column(String(120), nullable=True)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="reviews")
    restaurant = relationship("Restaurant", back_populates="reviews")
    menu_item = relationship("MenuItem", back_populates="reviews")
    order = relationship("Order", back_populates="review")

    __table_args__ = (
        UniqueConstraint("order_id", "menu_item_id", name="uq_reviews_order_item"),
        CheckConstraint("rating >= 1 AND rating <= 5", name="ck_reviews_rating_range"),
        Index("ix_reviews_menu_item_rating", "menu_item_id", "rating"),
    )

