"""
app/services/menu_service.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CoalSpark Restaurant — Menu Service

Handles all business logic for menu item operations:
  - List / search / filter items
  - Create new items
  - Partial update of items
  - Delete items (with image cleanup)
  - Upload / replace food images

Architecture note:
  This service is the ONLY layer that touches MenuItem rows.
  Routes call these functions; they never query the DB directly.
  This keeps route files thin and this file fully testable in
  isolation by injecting a mock session.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import os
import uuid
import shutil
from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import UploadFile

from app.models.menu_item import MenuItem, MenuCategory
from app.models.review import Review
from app.schemas.menu_item import MenuItemCreate, MenuItemUpdate
from app.utils.exceptions import not_found, bad_request
from app.core.config import settings


# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────

# Allowed MIME types for food image uploads
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/jpg", "image/png", "image/webp"}

# Mapping of MIME type to file extension
MIME_TO_EXT = {
    "image/jpeg": "jpg",
    "image/jpg":  "jpg",
    "image/png":  "png",
    "image/webp": "webp",
}


# ─────────────────────────────────────────────────────────────────────────────
# get_all_menu_items
# ─────────────────────────────────────────────────────────────────────────────
def get_all_menu_items(
    db: Session,
    category: Optional[str] = None,
    search: Optional[str] = None,
    is_available: Optional[bool] = True,
) -> List[MenuItem]:
    """
    Fetch menu items with optional category, search, and availability filters.

    Args:
        db           : DB session.
        category     : One of the MenuCategory enum values (e.g. "BBQ").
                       Case-sensitive to match the enum. Pass None for all.
        search       : Case-insensitive substring match on name OR description.
        is_available : True  → customer-facing menu (available items only).
                       False → show unavailable items only.
                       None  → no filter (admin view — shows everything).

    Returns:
        List[MenuItem] ordered by: featured items first, then name A→Z.

    Raises:
        HTTPException 400 : If `category` is provided but is not a valid enum value.

    Example queries:
        get_all_menu_items(db)                            # all available
        get_all_menu_items(db, category="BBQ")            # BBQ items only
        get_all_menu_items(db, search="chicken")          # search
        get_all_menu_items(db, is_available=None)         # admin: all items
    """
    avg_rating = func.coalesce(func.avg(Review.rating), 0.0).label("avg_rating")
    reviews_count = func.count(Review.id).label("reviews_count")
    query = (
        db.query(MenuItem, avg_rating, reviews_count)
        .outerjoin(Review, Review.menu_item_id == MenuItem.id)
        .group_by(MenuItem.id)
    )

    # ── Availability filter ───────────────────────────────────────────────────
    # None = no filter (admin sees everything, including unavailable items)
    if is_available is not None:
        query = query.filter(MenuItem.is_available == is_available)

    # ── Category filter ───────────────────────────────────────────────────────
    if category:
        # Normalize category: convert to lowercase to match enum member names
        # Frontend sends "BBQ" but database has "bbq"
        category_lower = category.lower().replace(" & ", "_").replace(" ", "_")
        
        # Validate against the enum member names
        valid_members = [c.name for c in MenuCategory]
        if category_lower not in valid_members:
            raise bad_request(
                f"Invalid category '{category}'. "
                f"Valid options are: {', '.join([c.value for c in MenuCategory])}"
            )
        
        # Get the enum member by name
        category_enum = getattr(MenuCategory, category_lower)
        query = query.filter(MenuItem.category == category_enum)

    # ── Full-text search (name + description) ─────────────────────────────────
    # ilike = case-insensitive LIKE in SQLAlchemy
    if search and search.strip():
        term = f"%{search.strip()}%"
        query = query.filter(
            MenuItem.name.ilike(term) |
            MenuItem.description.ilike(term)
        )

    # ── Ordering ──────────────────────────────────────────────────────────────
    # Featured items bubble to the top for the "Chef's Picks" section.
    # Within same featured status, sort alphabetically by name.
    query = query.order_by(
        MenuItem.is_featured.desc(),
        MenuItem.name.asc(),
    )

    rows = query.all()
    items: List[MenuItem] = []
    for item, ar, rc in rows:
        # attach computed fields for Pydantic response_model
        item.avg_rating = float(ar or 0.0)
        item.reviews_count = int(rc or 0)
        items.append(item)
    return items


# ─────────────────────────────────────────────────────────────────────────────
# get_menu_item_by_id
# ─────────────────────────────────────────────────────────────────────────────
def get_menu_item_by_id(db: Session, item_id: int) -> MenuItem:
    """
    Fetch a single menu item by its primary key.

    Args:
        db      : DB session.
        item_id : Primary key of the MenuItem row.

    Returns:
        MenuItem ORM instance.

    Raises:
        HTTPException 404 : If no item with the given ID exists.
    """
    avg_rating = func.coalesce(func.avg(Review.rating), 0.0).label("avg_rating")
    reviews_count = func.count(Review.id).label("reviews_count")
    row = (
        db.query(MenuItem, avg_rating, reviews_count)
        .outerjoin(Review, Review.menu_item_id == MenuItem.id)
        .filter(MenuItem.id == item_id)
        .group_by(MenuItem.id)
        .first()
    )

    if not row:
        raise not_found(f"Menu item #{item_id}")

    item, ar, rc = row
    item.avg_rating = float(ar or 0.0)
    item.reviews_count = int(rc or 0)
    return item


# ─────────────────────────────────────────────────────────────────────────────
# create_menu_item
# ─────────────────────────────────────────────────────────────────────────────
def create_menu_item(db: Session, data: MenuItemCreate) -> MenuItem:
    """
    Create a new menu item in the database.

    The image can be uploaded separately after creation using
    upload_item_image(). This two-step approach keeps the create
    endpoint simple (JSON body only, no multipart).

    Args:
        db   : DB session.
        data : Validated MenuItemCreate schema — all required fields included.

    Returns:
        MenuItem : The newly created and committed ORM instance with DB-assigned id.

    Note:
        - price is rounded to 2 decimal places by the Pydantic validator.
        - spice_level must be 1–5 (validated in schema).
        - image_url starts as None; set it with upload_item_image().
    """
    # Unpack schema into model kwargs
    item = MenuItem(**data.model_dump())

    db.add(item)
    db.commit()
    db.refresh(item)

    return item


# ─────────────────────────────────────────────────────────────────────────────
# update_menu_item
# ─────────────────────────────────────────────────────────────────────────────
def update_menu_item(db: Session, item_id: int, data: MenuItemUpdate) -> MenuItem:
    """
    Partially update a menu item.

    Uses Pydantic's model_dump(exclude_unset=True) so only explicitly
    provided fields are written to the database. Fields omitted from the
    request body retain their current database values.

    Args:
        db      : DB session.
        item_id : Primary key of the item to update.
        data    : MenuItemUpdate schema — any combination of updatable fields.

    Returns:
        MenuItem : The updated ORM instance after commit.

    Raises:
        HTTPException 404 : If the item does not exist.

    Example:
        To toggle availability only:
            update_menu_item(db, 5, MenuItemUpdate(is_available=False))
        To change price only:
            update_menu_item(db, 5, MenuItemUpdate(price=349.00))
    """
    # 1. Fetch or 404
    item = get_menu_item_by_id(db, item_id)

    # 2. Get only the fields that were explicitly sent in the request
    update_data = data.model_dump(exclude_unset=True)

    if not update_data:
        # No fields to update — return current state unchanged
        return item

    # 3. Apply each field
    for field, value in update_data.items():
        setattr(item, field, value)

    # 4. Persist
    db.commit()
    db.refresh(item)

    return item


# ─────────────────────────────────────────────────────────────────────────────
# delete_menu_item
# ─────────────────────────────────────────────────────────────────────────────
def delete_menu_item(db: Session, item_id: int) -> dict:
    """
    Permanently delete a menu item and clean up its image file.

    Database cascade behaviour:
        order_items.menu_item_id has ON DELETE SET NULL, so existing
        order line items are preserved but their menu_item_id is nulled.
        This keeps historical order data intact.

    Args:
        db      : DB session.
        item_id : Primary key of the item to delete.

    Returns:
        dict : Confirmation message with the deleted item name.

    Raises:
        HTTPException 404 : If the item does not exist.
    """
    # 1. Fetch or 404
    item = get_menu_item_by_id(db, item_id)
    item_name = item.name   # capture before deletion

    # 2. Delete image file from disk if it exists
    if item.image_url:
        # image_url is stored as "/uploads/filename.jpg"
        # Strip the leading "/" to get the relative path from the project root
        disk_path = item.image_url.lstrip("/")
        if os.path.isfile(disk_path):
            try:
                os.remove(disk_path)
            except OSError as e:
                # Log but don't block deletion — DB cleanup is more important
                print(f"[WARNING] Could not delete image file {disk_path}: {e}")

    # 3. Delete DB row
    db.delete(item)
    db.commit()

    return {
        "message": f"Menu item '{item_name}' (id={item_id}) deleted successfully.",
        "deleted_id": item_id,
    }


# ─────────────────────────────────────────────────────────────────────────────
# upload_item_image
# ─────────────────────────────────────────────────────────────────────────────
def upload_item_image(db: Session, item_id: int, file: UploadFile) -> MenuItem:
    """
    Upload and attach a food image to a menu item.

    Process:
    1. Validate MIME type (JPEG, PNG, WebP only).
    2. Read file content and enforce size limit (MAX_FILE_SIZE from settings).
    3. Generate a UUID-based filename to avoid collisions and directory traversal.
    4. Ensure the uploads directory exists.
    5. Write the file to uploads/<uuid>.<ext>.
    6. Delete the previous image file from disk if one existed.
    7. Update menu_items.image_url in the database.
    8. Return the updated MenuItem.

    Args:
        db      : DB session.
        item_id : Primary key of the menu item to attach the image to.
        file    : FastAPI UploadFile object from the multipart form.

    Returns:
        MenuItem : Updated item with new image_url set.

    Raises:
        HTTPException 400 : If the file type is not allowed.
        HTTPException 400 : If the file exceeds the size limit.
        HTTPException 404 : If the menu item does not exist.

    Security:
        - UUID filenames prevent directory traversal attacks.
        - MIME type is validated against an allowlist.
        - File size is checked before writing to disk.
    """
    # ── 1. Fetch item or 404 ──────────────────────────────────────────────────
    item = get_menu_item_by_id(db, item_id)

    # ── 2. Validate MIME type ─────────────────────────────────────────────────
    content_type = (file.content_type or "").lower()
    if content_type not in ALLOWED_IMAGE_TYPES:
        raise bad_request(
            f"File type '{content_type}' is not allowed. "
            f"Please upload a JPEG, PNG, or WebP image."
        )

    # ── 3. Read file content + size check ─────────────────────────────────────
    file_content = file.file.read()
    file_size = len(file_content)

    if file_size == 0:
        raise bad_request("The uploaded file is empty. Please select a valid image.")

    if file_size > settings.MAX_FILE_SIZE:
        max_mb = settings.MAX_FILE_SIZE / (1024 * 1024)
        actual_mb = file_size / (1024 * 1024)
        raise bad_request(
            f"File size {actual_mb:.1f}MB exceeds the {max_mb:.0f}MB limit. "
            f"Please compress the image and try again."
        )

    # ── 4. Build a safe unique filename ───────────────────────────────────────
    ext = MIME_TO_EXT.get(content_type, "jpg")
    unique_filename = f"{uuid.uuid4().hex}.{ext}"
    save_path = os.path.join(settings.UPLOAD_DIR, unique_filename)

    # ── 5. Ensure uploads directory exists ────────────────────────────────────
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

    # ── 6. Write file bytes to disk ───────────────────────────────────────────
    try:
        with open(save_path, "wb") as out:
            out.write(file_content)
    except IOError as e:
        raise bad_request(f"Failed to save image: {str(e)}")

    # ── 7. Delete previous image file ─────────────────────────────────────────
    if item.image_url:
        old_path = item.image_url.lstrip("/")
        if os.path.isfile(old_path) and old_path != save_path:
            try:
                os.remove(old_path)
            except OSError as e:
                print(f"[WARNING] Could not delete old image {old_path}: {e}")

    # ── 8. Update DB with new image URL ───────────────────────────────────────
    # The URL is relative to the server root and proxied by Vite in dev mode.
    # In production, Nginx or a CDN would serve the /uploads/ path.
    item.image_url = f"/uploads/{unique_filename}"

    db.commit()
    db.refresh(item)

    return item