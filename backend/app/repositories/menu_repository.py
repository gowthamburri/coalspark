"""
app/repositories/menu_repository.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CoalSpark Restaurant — Menu Repository

Data access layer for MenuItem model operations.
Handles all direct database queries for menu items.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.menu_item import MenuItem, MenuCategory
from app.repositories.base import BaseRepository


class MenuRepository(BaseRepository[MenuItem]):
    """
    Repository for MenuItem model with specialized query methods.
    
    Extends BaseRepository with menu-specific queries:
      - Filter by category and availability
      - Search by name/description
      - Featured items retrieval
      - Price range filtering
    """
    
    def __init__(self, db: Session):
        super().__init__(MenuItem, db)
    
    def get_available_items(
        self,
        category: Optional[str] = None,
        search: Optional[str] = None,
        limit: int = 100,
    ) -> List[MenuItem]:
        """
        Fetch available menu items with optional filters.
        
        Args:
            category : Filter by specific category (e.g., "BBQ").
            search   : Search term for name/description match.
            limit    : Maximum number of results.
        
        Returns:
            List of available MenuItem instances.
        """
        query = self.db.query(MenuItem).filter(
            MenuItem.is_available == True
        )
        
        # Category filter
        if category:
            query = query.filter(MenuItem.category == MenuCategory(category))
        
        # Full-text search on name and description
        if search and search.strip():
            term = f"%{search.strip()}%"
            query = query.filter(
                or_(
                    MenuItem.name.ilike(term),
                    MenuItem.description.ilike(term),
                )
            )
        
        # Order: featured first, then alphabetical
        return (
            query.order_by(
                MenuItem.is_featured.desc(),
                MenuItem.name.asc(),
            )
            .limit(limit)
            .all()
        )
    
    def get_all_items(
        self,
        include_unavailable: bool = False,
        limit: int = 100,
    ) -> List[MenuItem]:
        """
        Fetch all menu items (including unavailable for admin view).
        
        Args:
            include_unavailable : If False, only available items returned.
            limit               : Maximum number of results.
        
        Returns:
            List of MenuItem instances.
        """
        query = self.db.query(MenuItem)
        
        if not include_unavailable:
            query = query.filter(MenuItem.is_available == True)
        
        return (
            query.order_by(
                MenuItem.is_featured.desc(),
                MenuItem.name.asc(),
            )
            .limit(limit)
            .all()
        )
    
    def get_featured_items(self, limit: int = 20) -> List[MenuItem]:
        """
        Fetch all featured menu items (Chef's Picks).
        
        Args:
            limit : Maximum number of results.
        
        Returns:
            List of featured MenuItem instances.
        """
        return (
            self.db.query(MenuItem)
            .filter(MenuItem.is_featured == True)
            .filter(MenuItem.is_available == True)
            .order_by(MenuItem.name.asc())
            .limit(limit)
            .all()
        )
    
    def get_items_by_category(
        self,
        category: str,
        available_only: bool = True,
        limit: int = 50,
    ) -> List[MenuItem]:
        """
        Fetch items in a specific category.
        
        Args:
            category       : Category enum value.
            available_only : If True, only return available items.
            limit          : Maximum number of results.
        
        Returns:
            List of MenuItem instances in the category.
        """
        query = self.db.query(MenuItem).filter(
            MenuItem.category == MenuCategory(category)
        )
        
        if available_only:
            query = query.filter(MenuItem.is_available == True)
        
        return query.order_by(MenuItem.name.asc()).limit(limit).all()
    
    def search_items(
        self,
        search_term: str,
        limit: int = 50,
    ) -> List[MenuItem]:
        """
        Search menu items by name or description.
        
        Args:
            search_term : Substring to search for.
            limit       : Maximum number of results.
        
        Returns:
            List of matching MenuItem instances.
        """
        term = f"%{search_term}%"
        return (
            self.db.query(MenuItem)
            .filter(
                or_(
                    MenuItem.name.ilike(term),
                    MenuItem.description.ilike(term),
                )
            )
            .filter(MenuItem.is_available == True)
            .order_by(MenuItem.is_featured.desc(), MenuItem.name.asc())
            .limit(limit)
            .all()
        )
    
    def get_items_by_price_range(
        self,
        min_price: float,
        max_price: float,
        limit: int = 50,
    ) -> List[MenuItem]:
        """
        Fetch items within a price range.
        
        Args:
            min_price : Minimum price (inclusive).
            max_price : Maximum price (inclusive).
            limit     : Maximum number of results.
        
        Returns:
            List of MenuItem instances in the price range.
        """
        return (
            self.db.query(MenuItem)
            .filter(
                MenuItem.is_available == True,
                MenuItem.price >= min_price,
                MenuItem.price <= max_price,
            )
            .order_by(MenuItem.price.asc())
            .limit(limit)
            .all()
        )
    
    def count_by_category(self, category: str) -> int:
        """
        Count items in a specific category.
        
        Args:
            category : Category enum value.
        
        Returns:
            Count of items in the category.
        """
        return (
            self.db.query(MenuItem)
            .filter(
                MenuItem.category == MenuCategory(category),
                MenuItem.is_available == True,
            )
            .count()
        )
    
    def get_low_stock_items(
        self,
        threshold: int = 5,
        limit: int = 20,
    ) -> List[MenuItem]:
        """
        Get items that are running low (if inventory tracking added).
        Currently returns featured items as placeholder.
        
        Args:
            threshold : Stock threshold.
            limit     : Maximum number of results.
        
        Returns:
            List of MenuItem instances.
        """
        # Placeholder - can be enhanced when inventory is tracked
        return self.get_featured_items(limit=limit)
