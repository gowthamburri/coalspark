"""
app/models/order_item.py
OrderItem — join table between orders and menu_items.
Stores the price snapshot at time of ordering.
"""
from sqlalchemy import Column, Integer, Float, ForeignKey, Index, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.session import Base


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id", ondelete="SET NULL"), nullable=True)
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Float, nullable=False)  # Price snapshot at order time
    subtotal = Column(Float, nullable=False)    # quantity * unit_price

    # Relationships
    order = relationship("Order", back_populates="order_items")
    menu_item = relationship("MenuItem", back_populates="order_items")

    __table_args__ = (
        Index("ix_order_items_order", "order_id"),
        UniqueConstraint("order_id", "menu_item_id", name="uq_order_items_order_menu_item"),
        CheckConstraint("quantity > 0", name="ck_order_items_quantity_positive"),
        CheckConstraint("unit_price >= 0", name="ck_order_items_unit_price_non_negative"),
        CheckConstraint("subtotal >= 0", name="ck_order_items_subtotal_non_negative"),
    )

    def __repr__(self):
        return f"<OrderItem order={self.order_id} item={self.menu_item_id} qty={self.quantity}>"