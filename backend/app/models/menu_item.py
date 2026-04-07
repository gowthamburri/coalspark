"""
app/models/menu_item.py
Menu item model — food items with category, price, and image.
"""
import enum
from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Float, Boolean,
    Text, DateTime, ForeignKey, Enum as SAEnum, Index, CheckConstraint
)
from sqlalchemy.orm import relationship
from app.db.session import Base


class MenuCategory(str, enum.Enum):
    bbq = "BBQ"
    biryani_mandi = "Biryani & Mandi"
    starters = "Starters"
    main_course = "Main Course"
    beverages = "Beverages"
    desserts = "Desserts"


class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    # Persist the enum's value (e.g. "BBQ") to the DB to match the
    # PostgreSQL ENUM values created by migrations. SQLAlchemy's Enum
    # can be configured to use the enum member values rather than names.
    category = Column(
        SAEnum(MenuCategory, values_callable=lambda enum_cls: [e.value for e in enum_cls], name="menucategory"),
        nullable=False,
        index=True,
    )
    image_url = Column(String(500), nullable=True)
    is_vegetarian = Column(Boolean, default=False)
    is_available = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    spice_level = Column(Integer, default=2)  # 1-5 scale
    preparation_time = Column(Integer, default=20)  # minutes
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    restaurant = relationship("Restaurant", back_populates="menu_items")
    order_items = relationship("OrderItem", back_populates="menu_item")
    reviews = relationship("Review", back_populates="menu_item")

    # Index for fast category + availability filtering
    __table_args__ = (
        Index("ix_menu_category_available", "category", "is_available"),
        Index("ix_menu_restaurant_category", "restaurant_id", "category"),
        CheckConstraint("price > 0", name="ck_menu_items_price_positive"),
        CheckConstraint("spice_level >= 1 AND spice_level <= 5", name="ck_menu_items_spice_level_range"),
        CheckConstraint("preparation_time > 0", name="ck_menu_items_prep_time_positive"),
    )

    def __repr__(self):
        return f"<MenuItem {self.name} ₹{self.price}>"