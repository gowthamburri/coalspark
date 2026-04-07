"""
app/api/router.py
Central API router for versioned endpoints.
"""

from fastapi import APIRouter

from app.api.routes import auth, menu, orders, restaurant, admin, coupons, reviews, payments

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(restaurant.router)
api_router.include_router(menu.router)
api_router.include_router(orders.router)
api_router.include_router(admin.router)
api_router.include_router(coupons.router)
api_router.include_router(reviews.router)
api_router.include_router(payments.router)

