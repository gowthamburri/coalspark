"""
app/api/routes/menu.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CoalSpark Restaurant — Menu Routes

Public endpoints (no auth required):
  GET  /api/v1/menu/            →  List all available menu items
  GET  /api/v1/menu/categories  →  List all category names
  GET  /api/v1/menu/{id}        →  Get a single menu item

Admin-only endpoints (requires Bearer token + admin role):
  POST   /api/v1/menu/           →  Create a new menu item
  PUT    /api/v1/menu/{id}       →  Update a menu item (partial)
  DELETE /api/v1/menu/{id}       →  Delete a menu item
  POST   /api/v1/menu/{id}/image →  Upload food image for item
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

from typing import Optional, List
from fastapi import APIRouter, Depends, Query, UploadFile, File, status, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.menu_item import MenuItemCreate, MenuItemRead, MenuItemUpdate
from app.services import menu_service
from app.utils.dependencies import require_admin
from app.models.menu_item import MenuCategory

# ── Router instance ───────────────────────────────────────────────────────────
router = APIRouter(
    prefix="/menu",
    tags=["Menu"],
)


# ═════════════════════════════════════════════════════════════════════════════
# PUBLIC ENDPOINTS — no authentication required
# ═════════════════════════════════════════════════════════════════════════════

# ─────────────────────────────────────────────────────────────────────────────
# GET /menu/
# ─────────────────────────────────────────────────────────────────────────────
@router.get(
    "/",
    response_model=List[MenuItemRead],
    status_code=status.HTTP_200_OK,
    summary="List all available menu items",
    description="""
    Returns all menu items where `is_available = true`.

    **Filtering:**
    - `category` — filter by one of: `BBQ`, `Biryani & Mandi`, `Starters`,
      `Main Course`, `Beverages`, `Desserts`
    - `search` — full-text search on item name and description (case-insensitive)

    **Ordering:** Featured items appear first, then alphabetical by name.
    """,
    responses={
        200: {"description": "List of menu items returned."},
        400: {"description": "Invalid category value."},
    },
)
def list_menu_items(
    category: Optional[str] = Query(
        None,
        description="Filter by category. One of: BBQ, Biryani & Mandi, Starters, Main Course, Beverages, Desserts",
        example="BBQ",
    ),
    search: Optional[str] = Query(
        None,
        description="Search by item name or description (case-insensitive).",
        example="chicken",
    ),
    db: Session = Depends(get_db),
):
    """
    ## List menu items

    The primary endpoint for the customer-facing menu page.

    ### Examples
    - All items:          `GET /menu/`
    - BBQ only:           `GET /menu/?category=BBQ`
    - Search chicken:     `GET /menu/?search=chicken`
    - BBQ + search:       `GET /menu/?category=BBQ&search=smoked`
    """
    return menu_service.get_all_menu_items(
        db,
        category=category,
        search=search,
        is_available=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# GET /menu/categories
# ─────────────────────────────────────────────────────────────────────────────
@router.get(
    "/categories",
    response_model=List[str],
    status_code=status.HTTP_200_OK,
    summary="Get all menu category names",
    description="Returns the list of all valid menu category names for use in filter UIs.",
)
def list_categories():
    """
    ## List categories

    Returns all valid `MenuCategory` enum values.
    Use these as values for the `category` query param in `GET /menu/`.
    """
    return [cat.value for cat in MenuCategory]


# ─────────────────────────────────────────────────────────────────────────────
# GET /menu/{item_id}
# ─────────────────────────────────────────────────────────────────────────────
@router.get(
    "/{item_id}",
    response_model=MenuItemRead,
    status_code=status.HTTP_200_OK,
    summary="Get a single menu item by ID",
    responses={
        200: {"description": "Menu item found."},
        404: {"description": "Menu item not found."},
    },
)
def get_menu_item(
    item_id: int,
    db: Session = Depends(get_db),
):
    """
    ## Get menu item

    Fetches full details of a single menu item by its primary key.
    Returns **404** if the ID does not exist.
    """
    return menu_service.get_menu_item_by_id(db, item_id)


# ═════════════════════════════════════════════════════════════════════════════
# ADMIN-ONLY ENDPOINTS — require Bearer token with role=admin
# ═════════════════════════════════════════════════════════════════════════════

# ─────────────────────────────────────────────────────────────────────────────
# POST /menu/
# ─────────────────────────────────────────────────────────────────────────────
@router.post(
    "/",
    response_model=MenuItemRead,
    status_code=status.HTTP_201_CREATED,
    summary="[Admin] Create a new menu item",
    description="""
    Creates a new item in the menu.
    **Requires admin role.**

    After creation, use `POST /menu/{id}/image` to upload the food photo.
    """,
    responses={
        201: {"description": "Menu item created."},
        400: {"description": "Validation failed (e.g. price ≤ 0, spice_level out of range)."},
        403: {"description": "Admin access required."},
    },
)
def create_menu_item(
    data: MenuItemCreate,
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),         # Guard: admin only
):
    """
    ## Create menu item

    ### Required fields
    | Field         | Type    | Notes                             |
    |---------------|---------|-----------------------------------|
    | name          | string  | Display name on the menu          |
    | price         | float   | Must be > 0 (stored as ₹)        |
    | category      | enum    | One of the 6 cuisine categories   |
    | restaurant_id | int     | ID of the parent restaurant       |

    ### Optional fields
    `description`, `is_vegetarian`, `is_available`, `is_featured`,
    `spice_level` (1–5), `preparation_time` (minutes)
    """
    return menu_service.create_menu_item(db, data)


# ─────────────────────────────────────────────────────────────────────────────
# PUT /menu/{item_id}
# ─────────────────────────────────────────────────────────────────────────────
@router.put(
    "/{item_id}",
    response_model=MenuItemRead,
    status_code=status.HTTP_200_OK,
    summary="[Admin] Update a menu item",
    description="""
    **Partial update** — only fields present in the request body are changed.
    Omitted fields retain their current values.
    **Requires admin role.**
    """,
    responses={
        200: {"description": "Menu item updated."},
        404: {"description": "Menu item not found."},
        403: {"description": "Admin access required."},
    },
)
def update_menu_item(
    item_id: int,
    data: MenuItemUpdate,
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),
):
    """
    ## Update menu item

    Uses `exclude_unset=True` under the hood — only the fields you send
    are written to the database. This makes it safe to toggle a single
    boolean (e.g. `{"is_available": false}`) without touching anything else.

    ### Common use cases
    - Toggle availability:   `{"is_available": false}`
    - Change price:          `{"price": 349.00}`
    - Feature an item:       `{"is_featured": true}`
    - Update description:    `{"description": "New description text"}`
    """
    return menu_service.update_menu_item(db, item_id, data)


# ─────────────────────────────────────────────────────────────────────────────
# DELETE /menu/{item_id}
# ─────────────────────────────────────────────────────────────────────────────
@router.delete(
    "/{item_id}",
    status_code=status.HTTP_200_OK,
    summary="[Admin] Delete a menu item",
    description="""
    Permanently deletes a menu item and its associated image file.
    **Requires admin role.**

    ⚠️ This also nullifies any `order_items` that referenced this item
    (via `ON DELETE SET NULL` on the foreign key).
    """,
    responses={
        200: {"description": "Menu item deleted."},
        404: {"description": "Menu item not found."},
        403: {"description": "Admin access required."},
    },
)
def delete_menu_item(
    item_id: int,
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),
):
    """
    ## Delete menu item

    Removes the item from `menu_items` and deletes its image file from disk.
    Returns a confirmation message on success.
    """
    return menu_service.delete_menu_item(db, item_id)


# ─────────────────────────────────────────────────────────────────────────────
# POST /menu/{item_id}/image
# ─────────────────────────────────────────────────────────────────────────────
@router.post(
    "/{item_id}/image",
    response_model=MenuItemRead,
    status_code=status.HTTP_200_OK,
    summary="[Admin] Upload a food photo for a menu item",
    description="""
    Uploads an image file and sets it as the menu item's photo.
    The image is saved to the `/uploads/` directory and served as a static file.

    **Accepted formats:** JPEG, PNG, WebP
    **Max size:** 5 MB
    **Requires admin role.**

    If the item already has an image, the old file is deleted and replaced.
    """,
    responses={
        200: {"description": "Image uploaded, item updated with new image_url."},
        400: {"description": "Invalid file type."},
        404: {"description": "Menu item not found."},
        403: {"description": "Admin access required."},
    },
)
def upload_image(
    item_id: int,
    file: UploadFile = File(
        ...,
        description="Image file to upload (JPEG, PNG, or WebP, max 5 MB).",
    ),
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),
):
    """
    ## Upload food image

    ### How it works
    1. Validates MIME type (`image/jpeg`, `image/png`, `image/webp`)
    2. Generates a UUID-based filename to avoid collisions
    3. Saves to `uploads/<uuid>.<ext>` on disk
    4. Deletes previous image if one existed
    5. Updates `menu_items.image_url = /uploads/<uuid>.<ext>`
    6. Returns the updated menu item

    The image is then accessible at `http://localhost:8000/uploads/<uuid>.<ext>`
    (or proxied through Vite at `http://localhost:5173/uploads/<uuid>.<ext>`).
    """
    # Guard: reject if no file provided
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No file provided.",
        )

    return menu_service.upload_item_image(db, item_id, file)