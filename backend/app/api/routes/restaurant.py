"""
app/api/routes/restaurant.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CoalSpark Restaurant — Restaurant Profile Routes

Public endpoints:
  GET  /api/v1/restaurant/         →  Get restaurant details
  GET  /api/v1/restaurant/status   →  Quick open/closed check

Admin-only endpoints:
  PUT   /api/v1/restaurant/        →  Update restaurant info
  PATCH /api/v1/restaurant/toggle  →  Toggle open/closed status
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.restaurant import RestaurantRead, RestaurantUpdate
from app.models.restaurant import Restaurant
from app.utils.dependencies import require_admin
from app.utils.exceptions import not_found

# ── Router instance ───────────────────────────────────────────────────────────
router = APIRouter(
    prefix="/restaurant",
    tags=["Restaurant"],
)


# ─────────────────────────────────────────────────────────────────────────────
# HELPER — get or seed restaurant
# ─────────────────────────────────────────────────────────────────────────────
def _get_or_seed(db: Session) -> Restaurant:
    """
    Fetch the first restaurant row.
    If none exists (fresh DB), seeds CoalSpark's default profile automatically.
    This makes the app work out-of-the-box without manual DB seeding.
    """
    restaurant = db.query(Restaurant).first()

    if not restaurant:
        restaurant = Restaurant(
            name="CoalSpark Multi Cuisine Restaurant",
            tagline="Where Fire Meets Flavour",
            description=(
                "Premium BBQ & multi-cuisine dining in the heart of Gachibowli, Hyderabad. "
                "Slow-smoked meats, aromatic biryanis, Mandi, and global flavours crafted with passion "
                "in our open kitchen. Every dish is a celebration of fire, spice, and technique."
            ),
            address="Plot 42, HITEC City Road, Gachibowli",
            city="Hyderabad",
            phone="+91 98765 43210",
            email="hello@coalspark.in",
            rating=4.7,
            total_reviews=1248,
            opening_time="11:00",
            closing_time="23:30",
            cuisine_types="BBQ, Biryani & Mandi, Starters, Main Course, Beverages, Desserts",
            is_open="true",
        )
        db.add(restaurant)
        db.commit()
        db.refresh(restaurant)

    return restaurant


# ═════════════════════════════════════════════════════════════════════════════
# PUBLIC ENDPOINTS
# ═════════════════════════════════════════════════════════════════════════════

# ─────────────────────────────────────────────────────────────────────────────
# GET /restaurant/
# ─────────────────────────────────────────────────────────────────────────────
@router.get(
    "/",
    response_model=RestaurantRead,
    status_code=status.HTTP_200_OK,
    summary="Get CoalSpark restaurant profile",
    description="""
    Returns the full restaurant profile including:
    - Name, tagline, description
    - Address and contact details
    - Rating and review count
    - Opening and closing times
    - Cuisine types offered
    - Open/closed status

    **No authentication required.**

    If the restaurant record doesn't exist yet (fresh database),
    it is automatically seeded with CoalSpark's default data.
    """,
    responses={
        200: {"description": "Restaurant profile returned."},
    },
)
def get_restaurant(
    db: Session = Depends(get_db),
):
    """
    ## Get restaurant profile

    The primary endpoint used by the frontend **Home** page to display
    restaurant details, ratings, hours, and location.

    ### Auto-seeding
    On a fresh database with no restaurant record, this endpoint seeds the
    default CoalSpark profile so the app is usable immediately without
    running separate seed scripts.

    ### Response example
    ```json
    {
        "id": 1,
        "name": "CoalSpark Multi Cuisine Restaurant",
        "tagline": "Where Fire Meets Flavour",
        "address": "Plot 42, HITEC City Road, Gachibowli",
        "city": "Hyderabad",
        "phone": "+91 98765 43210",
        "rating": 4.7,
        "total_reviews": 1248,
        "opening_time": "11:00",
        "closing_time": "23:30",
        "is_open": "true"
    }
    ```
    """
    return _get_or_seed(db)


# ─────────────────────────────────────────────────────────────────────────────
# GET /restaurant/status
# ─────────────────────────────────────────────────────────────────────────────
@router.get(
    "/status",
    status_code=status.HTTP_200_OK,
    summary="Quick check — is the restaurant currently open?",
    description="""
    Lightweight endpoint returning only the open/closed status.
    Use this for real-time availability banners in the UI without
    fetching the full restaurant profile.

    **No authentication required.**
    """,
    responses={
        200: {"description": "Status returned."},
    },
)
def restaurant_status(
    db: Session = Depends(get_db),
):
    """
    ## Restaurant open/closed status

    ### Response
    ```json
    {
        "is_open": true,
        "opening_time": "11:00",
        "closing_time": "23:30",
        "message": "We are open! Come on in."
    }
    ```
    """
    restaurant = _get_or_seed(db)
    is_open = restaurant.is_open.lower() == "true"

    return {
        "is_open": is_open,
        "opening_time": restaurant.opening_time,
        "closing_time": restaurant.closing_time,
        "message": (
            f"We are open! Kitchen closes at {restaurant.closing_time}."
            if is_open
            else f"We are currently closed. We open at {restaurant.opening_time}."
        ),
    }


# ═════════════════════════════════════════════════════════════════════════════
# ADMIN-ONLY ENDPOINTS
# ═════════════════════════════════════════════════════════════════════════════

# ─────────────────────────────────────────────────────────────────────────────
# PUT /restaurant/
# ─────────────────────────────────────────────────────────────────────────────
@router.put(
    "/",
    response_model=RestaurantRead,
    status_code=status.HTTP_200_OK,
    summary="[Admin] Update restaurant profile",
    description="""
    Partial update of the restaurant profile.
    Only fields included in the request body are modified.

    **Updatable fields:**
    `name`, `tagline`, `description`, `address`, `phone`, `email`,
    `opening_time`, `closing_time`, `is_open`

    **Requires admin role.**
    """,
    responses={
        200: {"description": "Restaurant profile updated."},
        404: {"description": "Restaurant record not found (run GET /restaurant/ first to seed it)."},
        403: {"description": "Admin access required."},
    },
)
def update_restaurant(
    data: RestaurantUpdate,
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),
):
    """
    ## Update restaurant profile

    Uses partial update pattern — only sends the fields you want to change.

    ### Example: update phone + closing time
    ```json
    {
        "phone": "+91 99999 88888",
        "closing_time": "23:00"
    }
    ```

    ### Example: close the restaurant temporarily
    ```json
    {"is_open": "false"}
    ```
    """
    restaurant = db.query(Restaurant).first()
    if not restaurant:
        raise not_found("Restaurant")

    update_fields = data.model_dump(exclude_unset=True)

    if not update_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update.",
        )

    for field, value in update_fields.items():
        setattr(restaurant, field, value)

    db.commit()
    db.refresh(restaurant)
    return restaurant


# ─────────────────────────────────────────────────────────────────────────────
# PATCH /restaurant/toggle
# ─────────────────────────────────────────────────────────────────────────────
@router.patch(
    "/toggle",
    response_model=RestaurantRead,
    status_code=status.HTTP_200_OK,
    summary="[Admin] Toggle restaurant open/closed status",
    description="""
    Flips `is_open` between `"true"` and `"false"`.
    A shortcut so admins don't need to send a full PUT request
    just to open or close the restaurant.

    **Requires admin role.**
    """,
    responses={
        200: {"description": "Status toggled."},
        404: {"description": "Restaurant not found."},
        403: {"description": "Admin access required."},
    },
)
def toggle_restaurant_status(
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),
):
    """
    ## Toggle open/closed

    Reads the current `is_open` value and flips it:
    - `"true"` → `"false"` (close the restaurant)
    - `"false"` → `"true"` (open the restaurant)

    Returns the updated restaurant profile.
    """
    restaurant = db.query(Restaurant).first()
    if not restaurant:
        raise not_found("Restaurant")

    # Flip the boolean stored as string
    current = restaurant.is_open.lower() == "true"
    restaurant.is_open = "false" if current else "true"

    db.commit()
    db.refresh(restaurant)
    return restaurant