"""
app/services/__init__.py
Central export point for all service layer functions.
"""

from app.services.auth_service import register_user, authenticate_user, generate_token
from app.services.menu_service import (
    get_all_menu_items,
    get_menu_item_by_id,
    create_menu_item,
    update_menu_item,
    delete_menu_item,
    upload_item_image,
)
from app.services.order_service import (
    create_order,
    get_user_orders,
    get_order_by_id,
    get_all_orders,
    update_order_status,
)
from app.services.admin_service import (
    get_dashboard_stats,
    get_all_users,
    get_user_by_id,
    toggle_user_active,
    get_recent_orders,
)
from app.services.coupon_service import (
    validate_coupon,
    create_coupon,
    list_coupons,
    update_coupon,
    delete_coupon,
)
from app.services.review_service import (
    create_review,
    list_item_reviews,
    list_my_reviews,
)

__all__ = [
    # Auth
    "register_user",
    "authenticate_user",
    "generate_token",
    # Menu
    "get_all_menu_items",
    "get_menu_item_by_id",
    "create_menu_item",
    "update_menu_item",
    "delete_menu_item",
    "upload_item_image",
    # Orders
    "create_order",
    "get_user_orders",
    "get_order_by_id",
    "get_all_orders",
    "update_order_status",
    # Admin
    "get_dashboard_stats",
    "get_all_users",
    "get_user_by_id",
    "toggle_user_active",
    "get_recent_orders",
    # Coupons
    "validate_coupon",
    "create_coupon",
    "list_coupons",
    "update_coupon",
    "delete_coupon",
    # Reviews
    "create_review",
    "list_item_reviews",
    "list_my_reviews",
]