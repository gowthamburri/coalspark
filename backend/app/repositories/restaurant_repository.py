"""
app/repositories/restaurant_repository.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CoalSpark Restaurant — Restaurant Repository

Data access layer for Restaurant model operations.
Handles all direct database queries for restaurant profile.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

from typing import Optional

from sqlalchemy.orm import Session

from app.models.restaurant import Restaurant
from app.repositories.base import BaseRepository


class RestaurantRepository(BaseRepository[Restaurant]):
    """
    Repository for Restaurant model with specialized query methods.
    
    Extends BaseRepository with restaurant-specific queries:
      - Get active restaurant profile
      - Update hours and contact info
      - Toggle open/close status
    
    Note: This system assumes a single primary restaurant record,
    but the repository supports multiple locations if needed.
    """
    
    def __init__(self, db: Session):
        super().__init__(Restaurant, db)
    
    def get_active_restaurant(self) -> Optional[Restaurant]:
        """
        Fetch the primary active restaurant profile.
        
        For multi-location support, this would return the
        flagship or default location.
        
        Returns:
            Restaurant instance if exists, None otherwise.
        """
        # Assuming single restaurant setup - fetch first record
        return self.db.query(Restaurant).first()
    
    def update_hours(
        self,
        restaurant_id: int,
        opening_time: str,
        closing_time: str,
    ) -> Optional[Restaurant]:
        """
        Update restaurant operating hours.
        
        Args:
            restaurant_id : Primary key of the restaurant.
            opening_time  : Opening time (e.g., "11:00").
            closing_time  : Closing time (e.g., "23:00").
        
        Returns:
            Updated Restaurant instance, or None if not found.
        """
        restaurant = self.get(restaurant_id)
        
        if not restaurant:
            return None
        
        restaurant.opening_time = opening_time
        restaurant.closing_time = closing_time
        
        self.db.commit()
        self.db.refresh(restaurant)
        
        return restaurant
    
    def toggle_open_status(self, restaurant_id: int) -> Optional[Restaurant]:
        """
        Toggle the restaurant's open/closed status.
        
        Used to temporarily close the restaurant for orders
        (outside hours, holidays, special circumstances).
        
        Args:
            restaurant_id : Primary key of the restaurant.
        
        Returns:
            Updated Restaurant instance with toggled status.
        """
        restaurant = self.get(restaurant_id)
        
        if not restaurant:
            return None
        
        # Toggle between "true" and "false" string values
        restaurant.is_open = "false" if restaurant.is_open == "true" else "true"
        
        self.db.commit()
        self.db.refresh(restaurant)
        
        return restaurant
    
    def update_contact_info(
        self,
        restaurant_id: int,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        address: Optional[str] = None,
    ) -> Optional[Restaurant]:
        """
        Update restaurant contact information.
        
        Args:
            restaurant_id : Primary key of the restaurant.
            phone         : New phone number.
            email         : New email address.
            address       : New physical address.
        
        Returns:
            Updated Restaurant instance, or None if not found.
        """
        restaurant = self.get(restaurant_id)
        
        if not restaurant:
            return None
        
        if phone is not None:
            restaurant.phone = phone
        if email is not None:
            restaurant.email = email
        if address is not None:
            restaurant.address = address
        
        self.db.commit()
        self.db.refresh(restaurant)
        
        return restaurant
    
    def update_branding(
        self,
        restaurant_id: int,
        name: Optional[str] = None,
        tagline: Optional[str] = None,
        description: Optional[str] = None,
        logo_url: Optional[str] = None,
        banner_url: Optional[str] = None,
    ) -> Optional[Restaurant]:
        """
        Update restaurant branding elements.
        
        Args:
            restaurant_id : Primary key of the restaurant.
            name          : New restaurant name.
            tagline       : New tagline/slogan.
            description   : New description.
            logo_url      : New logo image URL.
            banner_url    : New banner image URL.
        
        Returns:
            Updated Restaurant instance, or None if not found.
        """
        restaurant = self.get(restaurant_id)
        
        if not restaurant:
            return None
        
        if name is not None:
            restaurant.name = name
        if tagline is not None:
            restaurant.tagline = tagline
        if description is not None:
            restaurant.description = description
        if logo_url is not None:
            restaurant.logo_url = logo_url
        if banner_url is not None:
            restaurant.banner_url = banner_url
        
        self.db.commit()
        self.db.refresh(restaurant)
        
        return restaurant
    
    def update_cuisine_types(
        self,
        restaurant_id: int,
        cuisine_types: str,
    ) -> Optional[Restaurant]:
        """
        Update the list of cuisine types offered.
        
        Args:
            restaurant_id : Primary key of the restaurant.
            cuisine_types : Comma-separated list of cuisines.
        
        Returns:
            Updated Restaurant instance, or None if not found.
        """
        restaurant = self.get(restaurant_id)
        
        if not restaurant:
            return None
        
        restaurant.cuisine_types = cuisine_types
        
        self.db.commit()
        self.db.refresh(restaurant)
        
        return restaurant
