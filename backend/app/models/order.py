"""
app/models/order.py
Order model — tracks customer orders with status lifecycle.
"""
import enum
from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Float, DateTime,
    ForeignKey, Text, Enum as SAEnum, Index, Boolean, CheckConstraint
)
from sqlalchemy.orm import relationship
from app.db.session import Base


class OrderStatus(str, enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    preparing = "preparing"
    ready = "ready"
    delivered = "delivered"
    cancelled = "cancelled"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    status = Column(SAEnum(OrderStatus), default=OrderStatus.pending, nullable=False)
    total_amount = Column(Float, nullable=False)
    delivery_address = Column(Text, nullable=True)
    special_instructions = Column(Text, nullable=True)
    payment_method = Column(String(50), default="cash")
    payment_id = Column(String(128), nullable=True)
    is_paid = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    review = relationship("Review", back_populates="order", uselist=False, cascade="all, delete-orphan")

    # Index for fast user order history queries
    __table_args__ = (
        Index("ix_orders_user_status", "user_id", "status"),
        Index("ix_orders_created_at", "created_at"),
        CheckConstraint("total_amount >= 0", name="ck_orders_total_amount_non_negative"),
    )

    def __repr__(self):
        return f"<Order #{self.id} [{self.status}] ₹{self.total_amount}>"