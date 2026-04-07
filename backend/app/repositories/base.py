"""
app/repositories/base.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CoalSpark Restaurant — Base Repository

Generic base repository with common CRUD operations.
All specific repositories inherit from this class.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

from typing import Generic, List, Optional, TypeVar, Type
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.session import Base

# Generic type for models
ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    Generic repository with basic CRUD operations.
    
    Provides common database operations that are shared across
    all entities: get by ID, get all, create, update, delete.
    
    Usage:
        class UserRepository(BaseRepository[User]):
            pass
        
        user_repo = UserRepository(User, db_session)
    """
    
    def __init__(self, model: Type[ModelType], db: Session):
        """
        Initialize the repository with a specific model class.
        
        Args:
            model : SQLAlchemy model class (e.g., User, MenuItem).
            db    : SQLAlchemy database session.
        """
        self.model_class = model
        self.db = db
    
    def get(self, id: int) -> Optional[ModelType]:
        """
        Fetch a single record by its primary key.
        
        Args:
            id : Primary key value.
        
        Returns:
            Model instance if found, None otherwise.
        """
        return self.db.query(self.model_class).filter(
            self.model_class.id == id
        ).first()
    
    def get_all(self, limit: int = 100, offset: int = 0) -> List[ModelType]:
        """
        Fetch all records with pagination support.
        
        Args:
            limit  : Maximum number of records to return.
            offset : Number of records to skip.
        
        Returns:
            List of model instances.
        """
        return (
            self.db.query(self.model_class)
            .limit(limit)
            .offset(offset)
            .all()
        )
    
    def create(self, data: dict) -> ModelType:
        """
        Create a new record in the database.
        
        Args:
            data : Dictionary of field values to set.
        
        Returns:
            The newly created and committed model instance.
        """
        db_obj = self.model_class(**data)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
    
    def update(self, db_obj: ModelType, data: dict) -> ModelType:
        """
        Update an existing record.
        
        Args:
            db_obj : Existing model instance to update.
            data   : Dictionary of fields to update.
        
        Returns:
            Updated model instance after commit.
        """
        for field, value in data.items():
            setattr(db_obj, field, value)
        
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
    
    def delete(self, db_obj: ModelType) -> None:
        """
        Delete a record from the database.
        
        Args:
            db_obj : Model instance to delete.
        """
        self.db.delete(db_obj)
        self.db.commit()
    
    def count(self) -> int:
        """
        Count total number of records.
        
        Returns:
            Total count of rows in the table.
        """
        return self.db.query(func.count(self.model_class.id)).scalar() or 0
