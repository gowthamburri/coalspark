"""
app/core/razorpay_client.py
Razorpay client factory (server-side only).
"""

import razorpay

from app.core.config import settings
from app.utils.exceptions import server_error


def get_razorpay_client() -> razorpay.Client:
    if not settings.RAZORPAY_KEY_ID or not settings.RAZORPAY_KEY_SECRET:
        raise server_error("Razorpay keys are not configured on the server.")
    return razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

