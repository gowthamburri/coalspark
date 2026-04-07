from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.razorpay_client import get_razorpay_client
from app.db.session import get_db
from app.schemas.payment import (
    CreatePaymentRequest,
    CreatePaymentResponse,
    VerifyPaymentRequest,
    VerifyPaymentResponse,
)
from app.services import payment_service
from app.utils.dependencies import get_current_user
from app.models.user import User


router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post(
    "/create-order",
    response_model=CreatePaymentResponse,
    status_code=status.HTTP_200_OK,
    summary="Create Razorpay order (payment intent)",
)
def create_order(data: CreatePaymentRequest, _db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Create a Razorpay order and return order id, amount (paise), currency and public key id."""
    try:
        client = get_razorpay_client()
        amount_paise = int(round(data.amount * 100))
        order = client.order.create({
            "amount": amount_paise,
            "currency": data.currency,
            "payment_capture": 1,
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return CreatePaymentResponse(
        razorpay_order_id=order["id"],
        amount=order["amount"],
        currency=order["currency"],
        key_id=client.auth[0],
    )


@router.post("/verify", response_model=VerifyPaymentResponse)
def verify_payment(
    data: VerifyPaymentRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        # If amount was not provided by frontend, fetch it from Razorpay order
        amount = data.amount
        if amount is None:
            client = get_razorpay_client()
            rz_order = client.order.fetch(data.razorpay_order_id)
            # Razorpay returns amount in paise
            amount = rz_order.get("amount", 0) / 100.0

        order = payment_service.verify_and_create_order(
            db=db,
            user_id=current_user.id,
            razorpay_order_id=data.razorpay_order_id,
            razorpay_payment_id=data.razorpay_payment_id,
            razorpay_signature=data.razorpay_signature,
            amount_in_rupees=amount,
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return VerifyPaymentResponse(success=True, order_id=order.id, message="Payment verified and order created")

