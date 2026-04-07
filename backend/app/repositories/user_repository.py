"""
app/repositories/user_repository.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CoalSpark Restaurant — User Repository

Data access layer for User model operations.
Handles all direct database queries for users.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.user import User, UserRole
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """
    Repository for User model with specialized query methods.
    
    Extends BaseRepository with user-specific queries:
      - Find by email (case-insensitive)
      - Filter by role
      - Active/inactive user filtering
      - Email uniqueness checks
    """
    
    def __init__(self, db: Session):
        super().__init__(User, db)
    
    def get_by_email(self, email: str) -> Optional[User]:
        """
        Find a user by email address (case-insensitive).
        
        Args:
            email : Email address to search for.
        
        Returns:
            User instance if found, None otherwise.
        """
        return (
            self.db.query(User)
            .filter(User.email.ilike(email))
            .first()
        )
    
    def get_by_role(self, role: UserRole, limit: int = 100) -> List[User]:
        """
        Fetch all users with a specific role.
        
        Args:
            role  : User role enum value (user or admin).
            limit : Maximum number of records to return.
        
        Returns:
            List of User instances with the specified role.
        """
        return (
            self.db.query(User)
            .filter(User.role == role)
            .limit(limit)
            .all()
        )
    
    def get_active_users(self, limit: int = 100) -> List[User]:
        """
        Fetch all active users (is_active=True).
        
        Args:
            limit : Maximum number of records to return.
        
        Returns:
            List of active User instances.
        """
        return (
            self.db.query(User)
            .filter(User.is_active == True)
            .limit(limit)
            .all()
        )
    
    def get_inactive_users(self, limit: int = 100) -> List[User]:
        """
        Fetch all inactive users (is_active=False).
        
        Args:
            limit : Maximum number of records to return.
        
        Returns:
            List of inactive User instances.
        """
        return (
            self.db.query(User)
            .filter(User.is_active == False)
            .limit(limit)
            .all()
        )
    
    def email_exists(self, email: str, exclude_id: Optional[int] = None) -> bool:
        """
        Check if an email is already registered.
        
        Args:
            email     : Email to check.
            exclude_id: Optionally exclude a specific user ID
                       (useful when updating a user's email).
        
        Returns:
            True if email exists, False otherwise.
        """
        query = self.db.query(User).filter(User.email.ilike(email))
        
        if exclude_id:
            query = query.filter(User.id != exclude_id)
        
        return query.first() is not None
    
    def count_by_role(self, role: UserRole) -> int:
        """
        Count users with a specific role.
        
        Args:
            role : User role enum value.
        
        Returns:
            Count of users with the given role.
        """
        return (
            self.db.query(User)
            .filter(User.role == role)
            .count()
        )
    
    def search_by_name(self, search_term: str, limit: int = 50) -> List[User]:
        """
        Search users by name (case-insensitive partial match).
        
        Args:
            search_term : Substring to search for in full_name.
            limit       : Maximum number of results.
        
        Returns:
            List of matching User instances.
        """
        term = f"%{search_term}%"
        return (
            self.db.query(User)
            .filter(User.full_name.ilike(term))
            .order_by(User.created_at.desc())
            .limit(limit)
            .all()
        )
