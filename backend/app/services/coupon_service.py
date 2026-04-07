from datetime import datetime, timezone

from sqlalchemy.orm import Session
from typing import Optional

from app.models.coupon import Coupon, CouponType
from app.schemas.coupon import CouponCreate, CouponUpdate
from app.utils.exceptions import bad_request, not_found, already_exists


def calculate_discount(coupon: Coupon, subtotal: float) -> float:
    if coupon.discount_type == CouponType.percentage:
        discount = subtotal * (coupon.discount_value / 100)
    else:
        discount = coupon.discount_value
    if coupon.max_discount_amount is not None:
        discount = min(discount, coupon.max_discount_amount)
    return round(max(discount, 0), 2)


def validate_coupon(db: Session, code: str, subtotal: float) -> tuple[Optional[Coupon], str, float]:
    coupon = db.query(Coupon).filter(Coupon.code == code.strip().upper()).first()
    if not coupon:
        return None, "Coupon not found.", 0.0
    if not coupon.is_active:
        return None, "Coupon is inactive.", 0.0
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    if now < coupon.starts_at:
        return None, "Coupon is not active yet.", 0.0
    if now > coupon.expires_at:
        return None, "Coupon has expired.", 0.0
    if subtotal < coupon.min_order_amount:
        return None, f"Minimum order amount is {coupon.min_order_amount}.", 0.0
    if coupon.usage_limit is not None and coupon.used_count >= coupon.usage_limit:
        return None, "Coupon usage limit reached.", 0.0
    return coupon, "Coupon applied successfully.", calculate_discount(coupon, subtotal)


def create_coupon(db: Session, data: CouponCreate) -> Coupon:
    code = data.code.strip().upper()
    exists = db.query(Coupon).filter(Coupon.code == code).first()
    if exists:
        raise already_exists("Coupon code")
    coupon = Coupon(**data.model_dump(exclude={"code"}), code=code)
    db.add(coupon)
    db.commit()
    db.refresh(coupon)
    return coupon


def list_coupons(db: Session) -> list[Coupon]:
    return db.query(Coupon).order_by(Coupon.created_at.desc()).all()


def update_coupon(db: Session, coupon_id: int, data: CouponUpdate) -> Coupon:
    coupon = db.query(Coupon).filter(Coupon.id == coupon_id).first()
    if not coupon:
        raise not_found("Coupon")
    fields = data.model_dump(exclude_unset=True)
    if not fields:
        raise bad_request("No fields provided for update.")
    for key, value in fields.items():
        setattr(coupon, key, value)
    db.commit()
    db.refresh(coupon)
    return coupon


def delete_coupon(db: Session, coupon_id: int) -> None:
    coupon = db.query(Coupon).filter(Coupon.id == coupon_id).first()
    if not coupon:
        raise not_found("Coupon")
    db.delete(coupon)
    db.commit()

