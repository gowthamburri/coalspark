"""
app/repositories/__init__.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CoalSpark Restaurant — Repositories Package

Central export point for all repository classes.
Import from here instead of individual modules.

Usage:
    from app.repositories import (
        UserRepository,
        MenuRepository,
        OrderRepository,
        RestaurantRepository,
    )
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

from app.repositories.base import BaseRepository
from app.repositories.user_repository import UserRepository
from app.repositories.menu_repository import MenuRepository
from app.repositories.order_repository import OrderRepository
from app.repositories.restaurant_repository import RestaurantRepository


# Convenience function to get all repositories with a single DB session
class RepositoryContainer:
    """
    Container holding instances of all repositories.
    
    Provides a clean way to access all repositories through
    a single dependency injection.
    
    Usage in FastAPI routes:
        def get_repositories(db = Depends(get_db)):
            return RepositoryContainer(db)
        
        @router.get("/users")
        def get_users(repos: RepositoryContainer = Depends(get_repositories)):
            return repos.users.get_all()
    """
    
    def __init__(self, db):
        self.db = db
        self.users = UserRepository(db)
        self.menu = MenuRepository(db)
        self.orders = OrderRepository(db)
        self.restaurants = RestaurantRepository(db)


__all__ = [
    "BaseRepository",
    "UserRepository",
    "MenuRepository",
    "OrderRepository",
    "RestaurantRepository",
    "RepositoryContainer",
]
