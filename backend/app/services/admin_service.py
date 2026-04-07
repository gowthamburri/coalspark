"""
app/services/admin_service.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CoalSpark Restaurant — Admin Service

Handles all admin-specific business logic:
  - Dashboard aggregated statistics
  - User listing and retrieval
  - User account activation / deactivation

All functions in this service require the calling route to have
already verified admin role (via require_admin dependency).
This service itself does NOT repeat that check — it trusts
the route layer to have enforced it.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.user import User, UserRole
from app.models.order import Order, OrderStatus
from app.models.menu_item import MenuItem
from app.utils.exceptions import not_found


# ─────────────────────────────────────────────────────────────────────────────
# get_dashboard_stats
# ─────────────────────────────────────────────────────────────────────────────
def get_dashboard_stats(db: Session) -> dict:
    """
    Aggregate key metrics from the database for the admin dashboard.

    Runs multiple COUNT and SUM queries in sequence.
    All queries leverage the indexes defined on:
      - users.role + users.is_active         (ix_users_role_active)
      - orders.status                         (ix_orders_user_status)
      - orders.created_at                     (ix_orders_created_at)
      - menu_items.is_available               (ix_menu_category_available)

    Args:
        db : SQLAlchemy DB session.

    Returns:
        dict with the following keys:
          total_users        (int)   — count of accounts with role='user'
          total_orders       (int)   — all-time order count
          total_revenue      (float) — sum of non-cancelled order totals (₹)
          pending_orders     (int)   — orders with status='pending'
          total_menu_items   (int)   — count of available menu items
          orders_by_status   (dict)  — {status_name: count} breakdown
          top_items          (list)  — top 5 ordered menu items by quantity

    Performance note:
        Each stat is a separate query. In high-traffic production scenarios
        these could be cached (Redis) or combined into a single raw SQL CTE.
        For this application scale, sequential queries are perfectly fine.
    """

    # ── 1. Total customer accounts (excludes admins) ──────────────────────────
    total_users: int = (
        db.query(func.count(User.id))
        .filter(User.role == UserRole.user)
        .scalar() or 0
    )

    # ── 2. All-time order count ───────────────────────────────────────────────
    total_orders: int = (
        db.query(func.count(Order.id))
        .scalar() or 0
    )

    # ── 3. Revenue — sum of non-cancelled order totals ────────────────────────
    # Excludes cancelled orders to show "real" revenue only.
    total_revenue: float = (
        db.query(func.sum(Order.total_amount))
        .filter(Order.status != OrderStatus.cancelled)
        .scalar() or 0.0
    )

    # ── 4. Pending orders — need immediate kitchen attention ──────────────────
    pending_orders: int = (
        db.query(func.count(Order.id))
        .filter(Order.status == OrderStatus.pending)
        .scalar() or 0
    )

    # ── 5. Active menu items ──────────────────────────────────────────────────
    total_menu_items: int = (
        db.query(func.count(MenuItem.id))
        .filter(MenuItem.is_available == True)
        .scalar() or 0
    )

    # ── 6. Orders breakdown by every status ───────────────────────────────────
    # Iterate through all enum values and count separately so even 0-count
    # statuses appear in the response (no missing keys in the frontend).
    orders_by_status: dict = {}
    for status in OrderStatus:
        count = (
            db.query(func.count(Order.id))
            .filter(Order.status == status)
            .scalar() or 0
        )
        orders_by_status[status.value] = count

    # ── 7. Top 5 ordered items ────────────────────────────────────────────────
    # Joins order_items with menu_items to get name + total quantity ordered.
    from app.models.order_item import OrderItem

    top_items_query = (
        db.query(
            MenuItem.id,
            MenuItem.name,
            MenuItem.category,
            func.sum(OrderItem.quantity).label("total_ordered"),
            func.sum(OrderItem.subtotal).label("total_revenue"),
        )
        .join(OrderItem, OrderItem.menu_item_id == MenuItem.id)
        .group_by(MenuItem.id, MenuItem.name, MenuItem.category)
        .order_by(func.sum(OrderItem.quantity).desc())
        .limit(5)
        .all()
    )

    top_items = [
        {
            "id":            row.id,
            "name":          row.name,
            "category":      row.category.value if hasattr(row.category, 'value') else row.category,
            "total_ordered": int(row.total_ordered or 0),
            "total_revenue": round(float(row.total_revenue or 0), 2),
        }
        for row in top_items_query
    ]

    # ── Return combined stats dict ────────────────────────────────────────────
    return {
        "total_users":      total_users,
        "total_orders":     total_orders,
        "total_revenue":    round(float(total_revenue), 2),
        "pending_orders":   pending_orders,
        "total_menu_items": total_menu_items,
        "orders_by_status": orders_by_status,
        "top_items":        top_items,
    }


# ─────────────────────────────────────────────────────────────────────────────
# get_all_users
# ─────────────────────────────────────────────────────────────────────────────
def get_all_users(db: Session) -> List[User]:
    """
    Fetch all registered user accounts ordered by registration date (newest first).

    Returns both 'user' and 'admin' roles.
    Passwords (hashed_password) are excluded from the API response
    by the UserRead Pydantic schema — not at this level.

    Args:
        db : DB session.

    Returns:
        List[User] : All user ORM instances sorted newest → oldest.
    """
    return (
        db.query(User)
        .order_by(User.created_at.desc())
        .all()
    )


# ─────────────────────────────────────────────────────────────────────────────
# get_user_by_id
# ─────────────────────────────────────────────────────────────────────────────
def get_user_by_id(db: Session, user_id: int) -> User:
    """
    Fetch a single user by primary key.

    Args:
        db      : DB session.
        user_id : Primary key of the user to fetch.

    Returns:
        User : The ORM instance if found.

    Raises:
        HTTPException 404 : If no user with this ID exists.
    """
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise not_found(f"User #{user_id}")

    return user


# ─────────────────────────────────────────────────────────────────────────────
# toggle_user_active
# ─────────────────────────────────────────────────────────────────────────────
def toggle_user_active(db: Session, user_id: int) -> User:
    """
    Toggle a user account's active status between True and False.

    When is_active = False:
      - The user can no longer authenticate (login returns 401).
      - Any existing JWT tokens they hold will fail the get_current_user
        dependency check (which verifies is_active after decoding).
      - Their data (orders, etc.) is preserved — only login is blocked.

    When is_active = True:
      - The account is restored and the user can log in again.

    Args:
        db      : DB session.
        user_id : Primary key of the user to toggle.

    Returns:
        User : Updated user ORM instance with flipped is_active value.

    Raises:
        HTTPException 404 : If the user does not exist.

    Note:
        The admin route (admin.py) adds a safety guard preventing admins
        from toggling their own account. That check is in the route layer,
        not here, so this service remains generic and testable.
    """
    user = get_user_by_id(db, user_id)

    # Flip the boolean
    user.is_active = not user.is_active

    db.commit()
    db.refresh(user)

    return user


# ─────────────────────────────────────────────────────────────────────────────
# get_recent_orders  (bonus helper used in dashboard)
# ─────────────────────────────────────────────────────────────────────────────
def get_recent_orders(db: Session, limit: int = 10) -> List[Order]:
    """
    Fetch the N most recent orders across all users.

    Useful for a "Recent Activity" widget on the admin dashboard.

    Args:
        db    : DB session.
        limit : How many orders to return (default 10).

    Returns:
        List[Order] : Most recent orders with order_items loaded.
    """
    from sqlalchemy.orm import joinedload
    from app.models.order_item import OrderItem

    return (
        db.query(Order)
        .options(
            joinedload(Order.order_items)
            .joinedload(OrderItem.menu_item)
        )
        .order_by(Order.created_at.desc())
        .limit(limit)
        .all()
    )