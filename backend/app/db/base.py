"""
app/db/base.py
Imports all models so Alembic's autogenerate can detect them.
IMPORTANT: Every model must be imported here.
"""
from app.db.session import Base  # noqa: F401

# Import all models — Alembic needs to see them
from app.models.user import User  # noqa: F401
from app.models.restaurant import Restaurant  # noqa: F401
from app.models.menu_item import MenuItem  # noqa: F401
from app.models.order import Order  # noqa: F401
from app.models.order_item import OrderItem  # noqa: F401
from app.models.coupon import Coupon  # noqa: F401
from app.models.review import Review  # noqa: F401