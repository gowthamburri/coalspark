"""
app/services/order_service.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CoalSpark Restaurant — Order Service

Handles all business logic for customer and admin order operations:
  - Create a new order (with price snapshot + atomic transaction)
  - Fetch orders for a specific user (with full nested items)
  - Fetch a single order (with ownership enforcement)
  - Fetch all orders (admin)
  - Update order status (admin)

Key design decisions:
  - Price is captured at order time (unit_price = menu_item.price at that moment).
    Subsequent price changes to the menu item do NOT retroactively affect orders.
  - Order creation is a single atomic DB transaction — either all order_items
    are saved or none are (no partial orders in the database).
  - joinedload() is used on retrieval queries to avoid N+1 SELECT problems.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

from typing import List

from sqlalchemy.orm import Session, joinedload

from app.models.order import Order, OrderStatus
from app.models.order_item import OrderItem
from app.models.menu_item import MenuItem
from app.schemas.order import OrderCreate, OrderStatusUpdate
from app.services.coupon_service import validate_coupon
from app.utils.exceptions import not_found, bad_request


# ─────────────────────────────────────────────────────────────────────────────
# create_order
# ─────────────────────────────────────────────────────────────────────────────
def create_order(db: Session, data: OrderCreate, user_id: int) -> Order:
    """
    Create a new order for an authenticated user.

    This function is the most critical in the system — it must be correct,
    atomic, and secure. Here's exactly what it does:

    Validation (per line item):
      - Menu item must exist in the database.
      - Menu item must be currently available (is_available = True).
      - Quantity is already validated by Pydantic schema (1–20).

    Price snapshot:
      - unit_price is read from menu_items.price at the moment of ordering.
      - It is stored permanently in order_items.unit_price.
      - Future price changes to the menu item have NO effect on this order.

    Total calculation:
      - subtotal per line = quantity × unit_price (rounded to 2 decimal places)
      - total_amount = sum of all subtotals (rounded to 2 decimal places)
      - Taxes are NOT added here — they are calculated on the frontend for display.

    Transaction:
      - db.flush() assigns order.id without committing.
      - All order_items are added and then db.commit() saves everything at once.
      - If anything fails mid-way, the transaction is rolled back automatically.

    Args:
        db      : SQLAlchemy DB session.
        data    : Validated OrderCreate schema containing items list,
                  optional delivery address, special instructions, payment method.
        user_id : ID of the authenticated user placing the order.

    Returns:
        Order : Fully created Order with all order_items attached and committed.

    Raises:
        HTTPException 404 : If any menu_item_id does not exist.
        HTTPException 400 : If any menu item is currently unavailable.
    """
    total_amount = 0.0
    order_items_to_create: List[OrderItem] = []

    # ── Validate each line item and build order_items list ────────────────────
    for line in data.items:
        # Fetch the menu item — raises 404 if not found
        menu_item = (
            db.query(MenuItem)
            .filter(MenuItem.id == line.menu_item_id)
            .first()
        )

        if not menu_item:
            raise not_found(
                f"Menu item with id={line.menu_item_id} does not exist. "
                f"Please refresh your cart and try again."
            )

        # Reject unavailable items
        if not menu_item.is_available:
            raise bad_request(
                f"'{menu_item.name}' is currently unavailable. "
                f"Please remove it from your cart and try again."
            )

        # Capture price at this exact moment (snapshot)
        unit_price = round(menu_item.price, 2)
        subtotal   = round(unit_price * line.quantity, 2)
        total_amount += subtotal

        # Build the OrderItem (order_id set below after flush)
        order_items_to_create.append(
            OrderItem(
                menu_item_id=menu_item.id,
                quantity=line.quantity,
                unit_price=unit_price,
                subtotal=subtotal,
            )
        )

    discount_amount = 0.0
    if data.coupon_code:
        coupon, message, discount_amount = validate_coupon(db, data.coupon_code, round(total_amount, 2))
        if not coupon:
            raise bad_request(message)
        total_amount = max(round(total_amount - discount_amount, 2), 0.0)
        coupon.used_count += 1

    # ── Create the parent Order ───────────────────────────────────────────────
    order = Order(
        user_id=user_id,
        total_amount=round(total_amount, 2),
        delivery_address=data.delivery_address,
        special_instructions=data.special_instructions,
        payment_method=data.payment_method,
        status=OrderStatus.pending,     # all orders start as pending
        is_paid=False,
    )
    db.add(order)

    # flush() writes the Order row and generates order.id
    # WITHOUT committing the transaction — critical for atomicity
    db.flush()

    # ── Attach OrderItems now that we have order.id ───────────────────────────
    for oi in order_items_to_create:
        oi.order_id = order.id
        db.add(oi)

    # ── Single atomic commit ──────────────────────────────────────────────────
    # If anything above raised an exception, this commit is never reached
    # and SQLAlchemy automatically rolls back the transaction.
    db.commit()

    # Reload with relationships to return the fully populated order
    db.refresh(order)
    return _load_order_with_items(db, order.id)


# ─────────────────────────────────────────────────────────────────────────────
# get_user_orders
# ─────────────────────────────────────────────────────────────────────────────
def get_user_orders(db: Session, user_id: int) -> List[Order]:
    """
    Fetch all orders placed by a specific user, newest first.

    Uses joinedload to eagerly fetch:
      orders → order_items → menu_item
    in a single SQL query, avoiding N+1 SELECT problems.

    Args:
        db      : DB session.
        user_id : ID of the authenticated user.

    Returns:
        List[Order] : All orders for this user, sorted newest → oldest.
                      Returns an empty list if no orders exist yet.
    """
    return (
        db.query(Order)
        .options(
            joinedload(Order.order_items)
            .joinedload(OrderItem.menu_item)
        )
        .filter(Order.user_id == user_id)
        .order_by(Order.created_at.desc())
        .all()
    )


# ─────────────────────────────────────────────────────────────────────────────
# get_order_by_id
# ─────────────────────────────────────────────────────────────────────────────
def get_order_by_id(db: Session, order_id: int, user_id: int) -> Order:
    """
    Fetch a specific order by ID, enforcing user ownership.

    The user_id check is intentional security — users must NOT be able
    to view each other's orders. We filter on BOTH order.id AND order.user_id.

    If either condition fails, we return 404 (not 403). This is deliberate:
    revealing "this order exists but it's not yours" would leak information
    about other users' orders (IDOR vulnerability).

    Args:
        db       : DB session.
        order_id : The ID of the order to fetch.
        user_id  : The ID of the requesting user.

    Returns:
        Order : The requested order with nested items loaded.

    Raises:
        HTTPException 404 : If the order doesn't exist OR doesn't belong
                            to the requesting user.
    """
    order = (
        db.query(Order)
        .options(
            joinedload(Order.order_items)
            .joinedload(OrderItem.menu_item)
        )
        .filter(
            Order.id      == order_id,
            Order.user_id == user_id,    # ownership check
        )
        .first()
    )

    if not order:
        raise not_found(f"Order #{order_id}")

    return order


# ─────────────────────────────────────────────────────────────────────────────
# get_all_orders  (admin)
# ─────────────────────────────────────────────────────────────────────────────
def get_all_orders(db: Session) -> List[Order]:
    """
    Fetch ALL orders from ALL users. Admin use only.

    No ownership filter — returns the entire orders table.
    The admin route (api/routes/admin.py) is responsible for
    ensuring only admins can call this.

    Args:
        db : DB session.

    Returns:
        List[Order] : All orders, newest first, with nested items loaded.
    """
    return (
        db.query(Order)
        .options(
            joinedload(Order.order_items)
            .joinedload(OrderItem.menu_item)
        )
        .order_by(Order.created_at.desc())
        .all()
    )


# ─────────────────────────────────────────────────────────────────────────────
# update_order_status  (admin)
# ─────────────────────────────────────────────────────────────────────────────
def update_order_status(
    db: Session,
    order_id: int,
    data: OrderStatusUpdate,
) -> Order:
    """
    Update the status of any order. Admin use only.

    Admins can set any status regardless of the current status.
    For customer-side cancellation (pending → cancelled only),
    see the orders route DELETE /orders/{id} which has additional
    business logic.

    Args:
        db       : DB session.
        order_id : The ID of the order to update.
        data     : OrderStatusUpdate schema — contains the new status value.

    Returns:
        Order : Updated order with new status, with nested items loaded.

    Raises:
        HTTPException 404 : If the order does not exist.
    """
    # Fetch without user_id filter — admins can update any order
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise not_found(f"Order #{order_id}")

    # Apply the status change
    order.status = data.status

    db.commit()

    # Reload with relationships
    return _load_order_with_items(db, order.id)


# ─────────────────────────────────────────────────────────────────────────────
# PRIVATE HELPER
# ─────────────────────────────────────────────────────────────────────────────
def _load_order_with_items(db: Session, order_id: int) -> Order:
    """
    Internal helper: reload a single order with all relationships eager-loaded.

    Used after create/update operations where db.refresh() would not
    automatically trigger joinedload of nested relationships.

    Args:
        db       : DB session.
        order_id : Primary key of the order to reload.

    Returns:
        Order with order_items and their menu_items loaded.
    """
    return (
        db.query(Order)
        .options(
            joinedload(Order.order_items)
            .joinedload(OrderItem.menu_item)
        )
        .filter(Order.id == order_id)
        .one()
    )