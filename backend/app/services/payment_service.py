from uuid import uuid4
from typing import Dict

import razorpay
from sqlalchemy.orm import Session

from app.models.order import Order, OrderStatus
from app.core.razorpay_client import get_razorpay_client


def create_razorpay_order(amount_in_rupees: float) -> Dict:
    """Create a Razorpay order and return the order payload.

    amount_in_rupees: amount in INR (e.g. 499.0)
    Returns dict with at least: id, amount, currency
    """
    client = get_razorpay_client()
    amount_paise = int(round(amount_in_rupees * 100))
    receipt = f"rcpt_{uuid4().hex[:12]}"
    order = client.order.create({
        "amount": amount_paise,
        "currency": "INR",
        "receipt": receipt,
        "payment_capture": 1,
    })
    return order


def verify_and_create_order(
    db: Session,
    user_id: int,
    razorpay_order_id: str,
    razorpay_payment_id: str,
    razorpay_signature: str,
    amount_in_rupees: float,
) -> Order:
    """Verify the signature using Razorpay utility and create Order in DB.

    Raises razorpay.errors.SignatureVerificationError on invalid signature.
    """
    client = get_razorpay_client()
    payload = {
        "razorpay_order_id": razorpay_order_id,
        "razorpay_payment_id": razorpay_payment_id,
        "razorpay_signature": razorpay_signature,
    }
    client.utility.verify_payment_signature(payload)

    # Signature valid — create order in DB and mark as paid
    order = Order(
        user_id=user_id,
        total_amount=amount_in_rupees,
        status=OrderStatus.pending,
        payment_method="razorpay",
        payment_id=razorpay_payment_id,
        is_paid=True,
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order
