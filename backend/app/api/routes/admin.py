"""
app/api/routes/admin.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CoalSpark Restaurant — Admin-Only Routes

ALL endpoints in this router require:
  1. A valid Bearer JWT token
  2. The token's user must have role = "admin"

If either condition fails → 401 or 403 is returned.

Endpoints:
  GET    /api/v1/admin/dashboard              →  Aggregated stats
  GET    /api/v1/admin/orders                 →  All orders (all users)
  GET    /api/v1/admin/orders/{id}            →  Single order detail
  PATCH  /api/v1/admin/orders/{id}/status     →  Update order status
  GET    /api/v1/admin/users                  →  All registered users
  GET    /api/v1/admin/users/{id}             →  Single user detail
  PATCH  /api/v1/admin/users/{id}/toggle      →  Activate/deactivate user
  GET    /api/v1/admin/menu                   →  All menu items (incl. unavailable)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.order import OrderRead, OrderStatusUpdate
from app.schemas.user import UserRead
from app.schemas.menu_item import MenuItemRead
from app.services import admin_service, order_service, menu_service
from app.utils.dependencies import require_admin
from app.models.user import User

# ── Router instance ───────────────────────────────────────────────────────────
router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


# ═════════════════════════════════════════════════════════════════════════════
# DASHBOARD
# ═════════════════════════════════════════════════════════════════════════════

@router.get(
    "/dashboard",
    status_code=status.HTTP_200_OK,
    summary="[Admin] Get aggregated dashboard statistics",
    description="""
    Returns real-time aggregated metrics for the admin dashboard.

    **Metrics returned:**
    - `total_users` — count of customer accounts
    - `total_orders` — all-time order count
    - `total_revenue` — sum of all non-cancelled order totals (₹)
    - `pending_orders` — orders awaiting confirmation
    - `total_menu_items` — count of currently available menu items
    - `orders_by_status` — breakdown by each status value

    **Requires admin role.**
    """,
    responses={
        200: {"description": "Dashboard stats returned."},
        403: {"description": "Admin access required."},
    },
)
def dashboard_stats(
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    """
    ## Dashboard stats

    Runs multiple `COUNT` and `SUM` aggregation queries against the database.
    All queries are optimised with indexes on `role`, `status`, and `created_at`.

    ### Response shape
    ```json
    {
        "total_users": 142,
        "total_orders": 389,
        "total_revenue": 287450.50,
        "pending_orders": 12,
        "total_menu_items": 48,
        "orders_by_status": {
            "pending": 12,
            "confirmed": 5,
            "preparing": 8,
            "ready": 3,
            "delivered": 354,
            "cancelled": 7
        }
    }
    ```
    """
    return admin_service.get_dashboard_stats(db)


# ═════════════════════════════════════════════════════════════════════════════
# ORDERS MANAGEMENT
# ═════════════════════════════════════════════════════════════════════════════

@router.get(
    "/orders",
    response_model=List[OrderRead],
    status_code=status.HTTP_200_OK,
    summary="[Admin] Get all orders across all users",
    description="""
    Returns every order in the system, sorted by `created_at` descending.
    Each order includes its nested `order_items` with menu item details.

    **Requires admin role.**
    """,
    responses={
        200: {"description": "All orders returned."},
        403: {"description": "Admin access required."},
    },
)
def all_orders(
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    """
    ## All orders

    Uses `joinedload` to eagerly load:
    ```
    orders → order_items → menu_item
    ```
    in a single query to avoid N+1 issues.
    """
    return order_service.get_all_orders(db)


@router.get(
    "/orders/{order_id}",
    response_model=OrderRead,
    status_code=status.HTTP_200_OK,
    summary="[Admin] Get a single order by ID",
    description="Fetch full details of any order by ID. No user ownership check. **Requires admin role.**",
    responses={
        200: {"description": "Order found."},
        404: {"description": "Order not found."},
        403: {"description": "Admin access required."},
    },
)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    """
    ## Get any order

    Unlike `GET /orders/{id}` (customer endpoint), this does **not** check
    user ownership — admins can view any order.
    """
    from sqlalchemy.orm import joinedload
    from app.models.order import Order
    from app.models.order_item import OrderItem
    from app.utils.exceptions import not_found

    order = (
        db.query(Order)
        .options(joinedload(Order.order_items).joinedload(OrderItem.menu_item))
        .filter(Order.id == order_id)
        .first()
    )
    if not order:
        raise not_found("Order")
    return order


@router.patch(
    "/orders/{order_id}/status",
    response_model=OrderRead,
    status_code=status.HTTP_200_OK,
    summary="[Admin] Update an order's status",
    description="""
    Updates the status of any order to any valid `OrderStatus` value.

    **Valid statuses (in lifecycle order):**
    `pending` → `confirmed` → `preparing` → `ready` → `delivered`

    `cancelled` can be set from any state by an admin.

    **Requires admin role.**
    """,
    responses={
        200: {"description": "Order status updated."},
        404: {"description": "Order not found."},
        403: {"description": "Admin access required."},
        422: {"description": "Invalid status value."},
    },
)
def update_order_status(
    order_id: int,
    data: OrderStatusUpdate,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    """
    ## Update order status

    ### Request body
    ```json
    {"status": "confirmed"}
    ```

    ### Valid status values
    | Status    | Meaning                              |
    |-----------|--------------------------------------|
    | pending   | Order received, not yet confirmed    |
    | confirmed | Restaurant accepted the order        |
    | preparing | Kitchen is preparing the food        |
    | ready     | Food is ready for pickup/delivery    |
    | delivered | Order delivered to customer          |
    | cancelled | Order cancelled (any stage)          |
    """
    return order_service.update_order_status(db, order_id, data)


# ═════════════════════════════════════════════════════════════════════════════
# USER MANAGEMENT
# ═════════════════════════════════════════════════════════════════════════════

@router.get(
    "/users",
    response_model=List[UserRead],
    status_code=status.HTTP_200_OK,
    summary="[Admin] Get all registered users",
    description="""
    Returns all user accounts (both `user` and `admin` roles),
    sorted by registration date descending.

    **Requires admin role.**
    """,
    responses={
        200: {"description": "All users returned."},
        403: {"description": "Admin access required."},
    },
)
def all_users(
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    """
    ## All users

    Returns every row from the `users` table.
    Passwords are never included in responses (hashed_password is excluded by schema).
    """
    return admin_service.get_all_users(db)


@router.get(
    "/users/{user_id}",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
    summary="[Admin] Get a single user by ID",
    description="Fetch the profile of any user. **Requires admin role.**",
    responses={
        200: {"description": "User found."},
        404: {"description": "User not found."},
        403: {"description": "Admin access required."},
    },
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    """
    ## Get user by ID
    """
    from app.models.user import User as UserModel
    from app.utils.exceptions import not_found

    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise not_found("User")
    return user


@router.patch(
    "/users/{user_id}/toggle",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
    summary="[Admin] Toggle a user's active status",
    description="""
    Activates a deactivated account or deactivates an active one.
    Deactivated users receive a **403** on any authenticated request.

    **Requires admin role.**
    ⚠️ Admins cannot deactivate their own account via this endpoint.
    """,
    responses={
        200: {"description": "User active status toggled."},
        400: {"description": "Cannot deactivate your own account."},
        404: {"description": "User not found."},
        403: {"description": "Admin access required."},
    },
)
def toggle_user(
    user_id: int,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    """
    ## Toggle user active

    Flips `users.is_active` between `True` and `False`.

    ### Safety guard
    An admin cannot deactivate their own account — this would lock them
    out of the system permanently (there's no recovery route).
    """
    # Prevent self-lockout
    if _admin.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot deactivate your own admin account.",
        )
    return admin_service.toggle_user_active(db, user_id)


# ═════════════════════════════════════════════════════════════════════════════
# MENU (admin view — includes unavailable items)
# ═════════════════════════════════════════════════════════════════════════════

@router.get(
    "/menu",
    response_model=List[MenuItemRead],
    status_code=status.HTTP_200_OK,
    summary="[Admin] Get all menu items including unavailable ones",
    description="""
    Returns **all** menu items regardless of `is_available` status.
    The public `GET /menu/` endpoint filters out unavailable items.
    This endpoint is for the admin dashboard to see and manage everything.

    **Requires admin role.**
    """,
    responses={
        200: {"description": "All menu items returned."},
        403: {"description": "Admin access required."},
    },
)
def admin_menu(
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    """
    ## Admin menu view

    Same as `GET /menu/` but with `is_available=False` items included.
    Use this to manage the full catalogue including hidden/out-of-stock items.
    """
    return menu_service.get_all_menu_items(
        db,
        category=None,
        search=None,
        is_available=None,   # None = return all, no filter
    )