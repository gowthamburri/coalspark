"""
app/models/coupon.py
Coupon model for discount logic and validation windows.
"""
import enum
from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    Boolean,
    ForeignKey,
    Enum as SAEnum,
    CheckConstraint,
    Index,
)
from sqlalchemy.orm import relationship

from app.db.session import Base


class CouponType(str, enum.Enum):
    percentage = "percentage"
    fixed = "fixed"


class Coupon(Base):
    __tablename__ = "coupons"

    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id", ondelete="CASCADE"), nullable=False)
    code = Column(String(50), nullable=False, unique=True, index=True)
    discount_type = Column(SAEnum(CouponType), nullable=False, default=CouponType.percentage)
    discount_value = Column(Float, nullable=False)
    min_order_amount = Column(Float, nullable=False, default=0)
    max_discount_amount = Column(Float, nullable=True)
    usage_limit = Column(Integer, nullable=True)
    used_count = Column(Integer, nullable=False, default=0)
    starts_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    restaurant = relationship("Restaurant", back_populates="coupons")

    __table_args__ = (
        Index("ix_coupons_active_expiry", "is_active", "expires_at"),
        CheckConstraint("discount_value > 0", name="ck_coupons_discount_value_positive"),
        CheckConstraint("min_order_amount >= 0", name="ck_coupons_min_order_non_negative"),
        CheckConstraint("used_count >= 0", name="ck_coupons_used_count_non_negative"),
        CheckConstraint("usage_limit IS NULL OR usage_limit >= 0", name="ck_coupons_usage_limit_non_negative"),
        CheckConstraint(
            "(discount_type = 'percentage' AND discount_value <= 100) OR (discount_type = 'fixed')",
            name="ck_coupons_percentage_max_100",
        ),
        CheckConstraint("expires_at > starts_at", name="ck_coupons_expiry_after_start"),
    )

