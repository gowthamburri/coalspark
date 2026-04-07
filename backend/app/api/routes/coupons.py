from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.coupon import (
    CouponCreate,
    CouponRead,
    CouponUpdate,
    CouponValidateRequest,
    CouponValidateResponse,
)
from app.services import coupon_service
from app.utils.dependencies import require_admin

router = APIRouter(prefix="/coupons", tags=["Coupons"])


@router.post("/validate", response_model=CouponValidateResponse)
def validate_coupon(data: CouponValidateRequest, db: Session = Depends(get_db)):
    coupon, message, discount = coupon_service.validate_coupon(db, data.code, data.subtotal)
    final_total = round(max(data.subtotal - discount, 0), 2)
    return CouponValidateResponse(
        code=data.code,
        is_valid=coupon is not None,
        message=message,
        discount_amount=discount,
        final_total=final_total,
    )


@router.get("/", response_model=list[CouponRead], dependencies=[Depends(require_admin)])
def list_coupons(db: Session = Depends(get_db)):
    return coupon_service.list_coupons(db)


@router.post("/", response_model=CouponRead, dependencies=[Depends(require_admin)])
def create_coupon(data: CouponCreate, db: Session = Depends(get_db)):
    return coupon_service.create_coupon(db, data)


@router.patch("/{coupon_id}", response_model=CouponRead, dependencies=[Depends(require_admin)])
def update_coupon(coupon_id: int, data: CouponUpdate, db: Session = Depends(get_db)):
    return coupon_service.update_coupon(db, coupon_id, data)


@router.delete("/{coupon_id}", dependencies=[Depends(require_admin)])
def delete_coupon(coupon_id: int, db: Session = Depends(get_db)):
    coupon_service.delete_coupon(db, coupon_id)
    return {"message": "Coupon deleted"}

