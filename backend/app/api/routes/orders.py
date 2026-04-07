"""
app/api/routes/orders.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CoalSpark Restaurant — Customer Order Routes

All endpoints require a valid JWT (authenticated users only).

Endpoints:
  POST /api/v1/orders/           →  Place a new order
  GET  /api/v1/orders/me         →  Get all orders for current user
  GET  /api/v1/orders/{id}       →  Get a specific order by ID
  DELETE /api/v1/orders/{id}     →  Cancel an order (pending only)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.order import OrderCreate, OrderRead
from app.services import order_service
from app.utils.dependencies import get_current_user
from app.models.user import User
from app.models.order import OrderStatus

# ── Router instance ───────────────────────────────────────────────────────────
router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


# ─────────────────────────────────────────────────────────────────────────────
# POST /orders/
# ─────────────────────────────────────────────────────────────────────────────
@router.post(
    "/",
    response_model=OrderRead,
    status_code=status.HTTP_201_CREATED,
    summary="Place a new order",
    description="""
    Creates a new order for the authenticated user.

    **Validation performed:**
    - Each `menu_item_id` must exist in the database.
    - Each item must be currently available (`is_available = true`).
    - Quantity must be between 1 and 20 per line item.
    - `items` list must not be empty.

    **Price capture:** The unit price is read from the DB at order time
    and stored in `order_items.unit_price` — price changes after ordering
    do not affect existing orders.

    **Total:** Calculated server-side as `sum(quantity × unit_price)`.
    """,
    responses={
        201: {"description": "Order created successfully."},
        400: {"description": "Item unavailable or quantity out of range."},
        404: {"description": "One or more menu items not found."},
        401: {"description": "Not authenticated."},
    },
)
def place_order(
    data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    ## Place order

    ### Request body example
    ```json
    {
        "items": [
            {"menu_item_id": 3, "quantity": 2},
            {"menu_item_id": 7, "quantity": 1}
        ],
        "delivery_address": "Flat 4B, Cyber Pearl, Hitec City, Hyderabad",
        "special_instructions": "Extra spicy please, no onions",
        "payment_method": "upi"
    }
    ```

    ### Flow
    1. Validate each item exists and is available
    2. Snapshot `unit_price` from `menu_items.price`
    3. Calculate `subtotal = quantity × unit_price` per line
    4. Calculate `total_amount = sum of subtotals`
    5. INSERT `orders` row (status = `pending`)
    6. INSERT all `order_items` rows
    7. Commit atomically — either all succeed or nothing is saved
    8. Return complete order with nested items
    """
    return order_service.create_order(
        db,
        data=data,
        user_id=current_user.id,
    )


# ─────────────────────────────────────────────────────────────────────────────
# GET /orders/me
# ─────────────────────────────────────────────────────────────────────────────
@router.get(
    "/me",
    response_model=List[OrderRead],
    status_code=status.HTTP_200_OK,
    summary="Get all orders placed by the current user",
    description="""
    Returns the full order history for the authenticated user,
    sorted by `created_at` descending (newest first).

    Each order includes its nested `order_items` with menu item details.
    """,
    responses={
        200: {"description": "List of user's orders returned."},
        401: {"description": "Not authenticated."},
    },
)
def my_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    ## My order history

    Fetches all orders belonging to `current_user.id`.
    Uses `joinedload` to eagerly load `order_items → menu_item`
    in a single DB round-trip.

    Returns an empty list `[]` if no orders exist yet.
    """
    return order_service.get_user_orders(db, user_id=current_user.id)


# ─────────────────────────────────────────────────────────────────────────────
# GET /orders/{order_id}
# ─────────────────────────────────────────────────────────────────────────────
@router.get(
    "/{order_id}",
    response_model=OrderRead,
    status_code=status.HTTP_200_OK,
    summary="Get a specific order by ID",
    description="""
    Returns full details of a single order including all line items.

    **Security:** The order must belong to the authenticated user.
    Users cannot see each other's orders.
    Admins can use `GET /admin/orders` to see all orders.
    """,
    responses={
        200: {"description": "Order found and returned."},
        404: {"description": "Order not found or does not belong to this user."},
        401: {"description": "Not authenticated."},
    },
)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    ## Get single order

    Looks up `orders.id = order_id AND orders.user_id = current_user.id`.
    Returns **404** if either condition fails — intentionally does not
    reveal whether the order exists at all (prevents enumeration by other users).
    """
    return order_service.get_order_by_id(
        db,
        order_id=order_id,
        user_id=current_user.id,
    )


# ─────────────────────────────────────────────────────────────────────────────
# DELETE /orders/{order_id}
# ─────────────────────────────────────────────────────────────────────────────
@router.delete(
    "/{order_id}",
    status_code=status.HTTP_200_OK,
    summary="Cancel a pending order",
    description="""
    Allows a user to cancel their own order **only if it is still `pending`**.
    Once the order moves to `confirmed` or later, it cannot be cancelled by the customer.
    Admins can force-cancel any order via `PATCH /admin/orders/{id}/status`.
    """,
    responses={
        200: {"description": "Order cancelled successfully."},
        400: {"description": "Order cannot be cancelled (already confirmed or later)."},
        404: {"description": "Order not found or does not belong to this user."},
        401: {"description": "Not authenticated."},
    },
)
def cancel_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    ## Cancel order

    Business rule: customers can only cancel `pending` orders.

    ### Flow
    1. Fetch order (must belong to current user, else 404)
    2. Check `status == pending` (else raise 400)
    3. Set `status = cancelled`
    4. Commit and return confirmation
    """
    # 1. Fetch the order (ownership check included)
    order = order_service.get_order_by_id(
        db,
        order_id=order_id,
        user_id=current_user.id,
    )

    # 2. Only pending orders can be cancelled by the customer
    if order.status != OrderStatus.pending:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Order #{order_id} is already '{order.status.value}' "
                f"and cannot be cancelled. Contact the restaurant directly."
            ),
        )

    # 3. Cancel it
    order.status = OrderStatus.cancelled
    db.commit()
    db.refresh(order)

    return {
        "message": f"Order #{order_id} has been cancelled successfully.",
        "order_id": order_id,
        "status": "cancelled",
    }