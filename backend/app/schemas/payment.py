from pydantic import BaseModel, field_validator
from typing import Optional


class CreatePaymentRequest(BaseModel):
    amount: float  # in INR, e.g. 499.0
    currency: str = "INR"

    @field_validator("amount")
    @classmethod
    def positive_amount(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Amount must be greater than 0")
        return round(v, 2)


class CreatePaymentResponse(BaseModel):
    razorpay_order_id: str
    amount: int  # paise
    currency: str
    key_id: str


class VerifyPaymentRequest(BaseModel):
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str
    amount: Optional[float] = None  # in INR, e.g. 499.0; optional — will be fetched if missing


class VerifyPaymentResponse(BaseModel):
    success: bool
    order_id: Optional[int] = None
    message: str

