"""
app/db/init_db.py
Seed realistic sample data for local development.
"""
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models.user import User, UserRole
from app.models.restaurant import Restaurant
from app.models.menu_item import MenuItem, MenuCategory
from app.models.order import Order, OrderStatus
from app.models.order_item import OrderItem
from app.models.coupon import Coupon, CouponType
from app.models.review import Review


def seed(db: Session) -> None:
    admin = db.query(User).filter(User.email == "admin@coalspark.in").first()
    if not admin:
        admin = User(
            full_name="CoalSpark Admin",
            email="admin@coalspark.in",
            hashed_password=hash_password("Admin@12345"),
            role=UserRole.admin,
            is_active=True,
        )
        db.add(admin)

    user = db.query(User).filter(User.email == "customer@coalspark.in").first()
    if not user:
        user = User(
            full_name="Rahul Verma",
            email="customer@coalspark.in",
            hashed_password=hash_password("Customer@123"),
            role=UserRole.user,
            phone="+919999888777",
            is_active=True,
        )
        db.add(user)
    db.flush()

    restaurant = db.query(Restaurant).first()
    if not restaurant:
        restaurant = Restaurant(
            name="CoalSpark Multi Cuisine Restaurant",
            tagline="Where Fire Meets Flavor",
            description="Premium dark-theme BBQ and biryani destination in Gachibowli.",
            address="Gachibowli Main Road, Hyderabad",
            city="Hyderabad",
            phone="+914040401111",
            email="hello@coalspark.in",
            rating=4.6,
            total_reviews=412,
            is_open=True,
        )
        db.add(restaurant)
    db.flush()

    menu_seed = [
        ("Smoked BBQ Chicken", MenuCategory.bbq, 349.0, False, True),
        ("Hyderabadi Dum Biryani", MenuCategory.biryani_mandi, 389.0, False, True),
        ("Paneer Tikka Platter", MenuCategory.bbq, 299.0, True, False),
        ("Double Ka Meetha", MenuCategory.desserts, 149.0, True, False),
    ]
    for name, category, price, is_veg, is_featured in menu_seed:
        exists = db.query(MenuItem).filter(MenuItem.name == name).first()
        if not exists:
            db.add(
                MenuItem(
                    restaurant_id=restaurant.id,
                    name=name,
                    category=category,
                    price=price,
                    is_vegetarian=is_veg,
                    is_featured=is_featured,
                    is_available=True,
                    spice_level=2,
                    preparation_time=20,
                )
            )
    db.flush()

    coupon = db.query(Coupon).filter(Coupon.code == "BBQ20").first()
    if not coupon:
        db.add(
            Coupon(
                restaurant_id=restaurant.id,
                code="BBQ20",
                discount_type=CouponType.percentage,
                discount_value=20,
                min_order_amount=500,
                max_discount_amount=200,
                usage_limit=1000,
                starts_at=datetime.now(timezone.utc) - timedelta(days=2),
                expires_at=datetime.now(timezone.utc) + timedelta(days=45),
                is_active=True,
            )
        )

    delivered_order = db.query(Order).filter(Order.user_id == user.id, Order.status == OrderStatus.delivered).first()
    if not delivered_order:
        item = db.query(MenuItem).filter(MenuItem.name == "Smoked BBQ Chicken").first()
        delivered_order = Order(
            user_id=user.id,
            status=OrderStatus.delivered,
            total_amount=698.0,
            delivery_address="Kondapur, Hyderabad",
            payment_method="upi",
            is_paid=True,
        )
        db.add(delivered_order)
        db.flush()
        db.add(
            OrderItem(
                order_id=delivered_order.id,
                menu_item_id=item.id,
                quantity=2,
                unit_price=349.0,
                subtotal=698.0,
            )
        )

        db.add(
            Review(
                user_id=user.id,
                restaurant_id=restaurant.id,
                menu_item_id=item.id,
                order_id=delivered_order.id,
                rating=5,
                title="Outstanding BBQ",
                comment="Perfectly smoked and juicy. Will order again.",
            )
        )

    db.commit()


if __name__ == "__main__":
    session = SessionLocal()
    try:
        seed(session)
        print("Seed data inserted successfully.")
    finally:
        session.close()

