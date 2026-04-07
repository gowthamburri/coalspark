"""
app/repositories/order_repository.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CoalSpark Restaurant — Order Repository

Data access layer for Order model operations.
Handles all direct database queries for orders.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

from typing import List, Optional

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func

from app.models.order import Order, OrderStatus
from app.models.order_item import OrderItem
from app.repositories.base import BaseRepository


class OrderRepository(BaseRepository[Order]):
    """
    Repository for Order model with specialized query methods.
    
    Extends BaseRepository with order-specific queries:
      - User order history
      - Orders by status
      - Revenue calculations
      - Recent orders retrieval
    """
    
    def __init__(self, db: Session):
        super().__init__(Order, db)
    
    def get_user_orders(
        self,
        user_id: int,
        limit: int = 100,
    ) -> List[Order]:
        """
        Fetch all orders for a specific user (newest first).
        
        Uses eager loading to fetch order_items and menu_items
        in a single query to avoid N+1 problem.
        
        Args:
            user_id : ID of the user.
            limit   : Maximum number of results.
        
        Returns:
            List of Order instances with items loaded.
        """
        return (
            self.db.query(Order)
            .options(
                joinedload(Order.order_items)
                .joinedload(OrderItem.menu_item)
            )
            .filter(Order.user_id == user_id)
            .order_by(Order.created_at.desc())
            .limit(limit)
            .all()
        )
    
    def get_order_with_items(
        self,
        order_id: int,
        user_id: Optional[int] = None,
    ) -> Optional[Order]:
        """
        Fetch a single order with its items loaded.
        
        If user_id is provided, enforces ownership check.
        
        Args:
            order_id : Primary key of the order.
            user_id  : Optional user ID for ownership enforcement.
        
        Returns:
            Order instance with items loaded, or None if not found.
        """
        query = self.db.query(Order).options(
            joinedload(Order.order_items)
            .joinedload(OrderItem.menu_item)
        )
        
        if user_id:
            query = query.filter(
                Order.id == order_id,
                Order.user_id == user_id,
            )
        else:
            query = query.filter(Order.id == order_id)
        
        return query.first()
    
    def get_all_orders(
        self,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Order]:
        """
        Fetch all orders across all users (admin view).
        
        Args:
            limit  : Maximum number of results.
            offset : Number of records to skip.
        
        Returns:
            List of Order instances with items loaded.
        """
        return (
            self.db.query(Order)
            .options(
                joinedload(Order.order_items)
                .joinedload(OrderItem.menu_item)
            )
            .order_by(Order.created_at.desc())
            .limit(limit)
            .offset(offset)
            .all()
        )
    
    def get_orders_by_status(
        self,
        status: OrderStatus,
        limit: int = 50,
    ) -> List[Order]:
        """
        Fetch orders with a specific status.
        
        Args:
            status : Order status enum value.
            limit  : Maximum number of results.
        
        Returns:
            List of Order instances with the given status.
        """
        return (
            self.db.query(Order)
            .options(
                joinedload(Order.order_items)
                .joinedload(OrderItem.menu_item)
            )
            .filter(Order.status == status)
            .order_by(Order.created_at.asc())  # oldest first for kitchen queue
            .limit(limit)
            .all()
        )
    
    def get_pending_orders(self, limit: int = 50) -> List[Order]:
        """
        Fetch all pending orders awaiting confirmation.
        
        Args:
            limit : Maximum number of results.
        
        Returns:
            List of pending Order instances.
        """
        return self.get_orders_by_status(OrderStatus.pending, limit=limit)
    
    def get_recent_orders(
        self,
        limit: int = 20,
    ) -> List[Order]:
        """
        Fetch most recent orders across all users.
        
        Useful for admin dashboard "Recent Activity".
        
        Args:
            limit : Maximum number of results.
        
        Returns:
            List of recent Order instances.
        """
        return self.get_all_orders(limit=limit, offset=0)
    
    def count_by_status(self, status: OrderStatus) -> int:
        """
        Count orders with a specific status.
        
        Args:
            status : Order status enum value.
        
        Returns:
            Count of orders with the given status.
        """
        return (
            self.db.query(func.count(Order.id))
            .filter(Order.status == status)
            .scalar() or 0
        )
    
    def get_total_revenue(
        self,
        exclude_cancelled: bool = True,
    ) -> float:
        """
        Calculate total revenue from orders.
        
        Args:
            exclude_cancelled : If True, exclude cancelled orders.
        
        Returns:
            Total revenue as float.
        """
        query = self.db.query(func.sum(Order.total_amount))
        
        if exclude_cancelled:
            query = query.filter(Order.status != OrderStatus.cancelled)
        
        return query.scalar() or 0.0
    
    def get_orders_by_date_range(
        self,
        start_date,
        end_date,
        limit: int = 100,
    ) -> List[Order]:
        """
        Fetch orders within a date range.
        
        Args:
            start_date : Start datetime.
            end_date   : End datetime.
            limit      : Maximum number of results.
        
        Returns:
            List of Order instances in the date range.
        """
        return (
            self.db.query(Order)
            .options(
                joinedload(Order.order_items)
                .joinedload(OrderItem.menu_item)
            )
            .filter(
                Order.created_at >= start_date,
                Order.created_at <= end_date,
            )
            .order_by(Order.created_at.desc())
            .limit(limit)
            .all()
        )
    
    def get_top_selling_items(
        self,
        limit: int = 10,
    ) -> List[dict]:
        """
        Get top-selling menu items by quantity ordered.
        
        Args:
            limit : Maximum number of results.
        
        Returns:
            List of dicts with item details and total quantity sold.
        """
        from app.models.menu_item import MenuItem
        
        results = (
            self.db.query(
                MenuItem.id,
                MenuItem.name,
                MenuItem.category,
                func.sum(OrderItem.quantity).label("total_quantity"),
                func.sum(OrderItem.subtotal).label("total_revenue"),
            )
            .join(OrderItem, OrderItem.menu_item_id == MenuItem.id)
            .group_by(MenuItem.id, MenuItem.name, MenuItem.category)
            .order_by(func.sum(OrderItem.quantity).desc())
            .limit(limit)
            .all()
        )
        
        return [
            {
                "id": row.id,
                "name": row.name,
                "category": row.category.value if hasattr(row.category, 'value') else row.category,
                "total_quantity": int(row.total_quantity or 0),
                "total_revenue": round(float(row.total_revenue or 0), 2),
            }
            for row in results
        ]
