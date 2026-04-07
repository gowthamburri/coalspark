from sqlalchemy.orm import Session

from app.models.order import Order, OrderStatus
from app.models.order_item import OrderItem
from app.models.review import Review
from app.schemas.review import ReviewCreate
from app.utils.exceptions import bad_request, not_found


def create_review(db: Session, user_id: int, data: ReviewCreate) -> Review:
    order = db.query(Order).filter(Order.id == data.order_id, Order.user_id == user_id).first()
    if not order:
        raise not_found("Order")
    if order.status != OrderStatus.delivered:
        raise bad_request("You can rate items only after order delivery.")

    order_item = db.query(OrderItem).filter(
        OrderItem.order_id == data.order_id,
        OrderItem.menu_item_id == data.menu_item_id,
    ).first()
    if not order_item:
        raise bad_request("This item is not part of the order.")

    exists = db.query(Review).filter(
        Review.order_id == data.order_id,
        Review.menu_item_id == data.menu_item_id,
    ).first()
    if exists:
        raise bad_request("You have already reviewed this item for this order.")

    review = Review(
        user_id=user_id,
        order_id=data.order_id,
        menu_item_id=data.menu_item_id,
        restaurant_id=order_item.menu_item.restaurant_id,
        rating=data.rating,
        title=data.title,
        comment=data.comment,
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


def list_item_reviews(db: Session, menu_item_id: int) -> list[Review]:
    return db.query(Review).filter(Review.menu_item_id == menu_item_id).order_by(Review.created_at.desc()).all()


def list_my_reviews(db: Session, user_id: int) -> list[Review]:
    return db.query(Review).filter(Review.user_id == user_id).order_by(Review.created_at.desc()).all()

