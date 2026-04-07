# CoalSpark Backend Repositories

## Overview

The repository pattern provides a clean separation between business logic (services) and data access logic (repositories). This makes the codebase more maintainable, testable, and follows SOLID principles.

## Architecture

```
app/
├── models/          # SQLAlchemy ORM models
├── repositories/    # Data access layer ← YOU ARE HERE
├── services/        # Business logic layer
├── api/routes/      # HTTP endpoint handlers
└── schemas/         # Pydantic validation schemas
```

## Repository Structure

### Base Repository (`base.py`)

Generic CRUD operations available for all entities:

- `get(id)` - Fetch by primary key
- `get_all(limit, offset)` - List with pagination
- `create(data)` - Create new record
- `update(db_obj, data)` - Update existing record
- `delete(db_obj)` - Delete record
- `count()` - Count total records

### Specialized Repositories

Each entity has its own repository with custom query methods:

#### UserRepository
```python
from app.repositories import UserRepository

repo = UserRepository(db)

# Find by email (case-insensitive)
user = repo.get_by_email("admin@coalspark.in")

# Check email uniqueness
exists = repo.email_exists("test@example.com")

# Get users by role
users = repo.get_by_role(UserRole.user)

# Search by name
results = repo.search_by_name("john")

# Count by role
count = repo.count_by_role(UserRole.admin)
```

#### MenuRepository
```python
from app.repositories import MenuRepository

repo = MenuRepository(db)

# Get available items with filters
items = repo.get_available_items(
    category="BBQ",
    search="chicken"
)

# Get featured items (Chef's Picks)
featured = repo.get_featured_items()

# Filter by price range
items = repo.get_items_by_price_range(100, 500)

# Count by category
count = repo.count_by_category("Biryani & Mandi")
```

#### OrderRepository
```python
from app.repositories import OrderRepository

repo = OrderRepository(db)

# Get user's order history
orders = repo.get_user_orders(user_id=5)

# Get orders by status
pending = repo.get_pending_orders()

# Calculate total revenue
revenue = repo.get_total_revenue(exclude_cancelled=True)

# Get top-selling items
top_items = repo.get_top_selling_items(limit=10)

# Count by status
count = repo.count_by_status(OrderStatus.preparing)
```

#### RestaurantRepository
```python
from app.repositories import RestaurantRepository

repo = RestaurantRepository(db)

# Get active restaurant profile
restaurant = repo.get_active_restaurant()

# Toggle open/close status
repo.toggle_open_status(restaurant_id=1)

# Update hours
repo.update_hours(1, "11:00", "23:00")

# Update contact info
repo.update_contact_info(1, phone="+91 9876543210")
```

## Usage in Services

Repositories are used by service layer functions:

```python
# app/services/auth_service.py
from app.repositories import UserRepository

def register_user(db, data):
    user_repo = UserRepository(db)
    
    # Check if email exists
    if user_repo.email_exists(data.email):
        raise already_exists("An account with this email")
    
    # Create new user
    user = user_repo.create({
        "full_name": data.full_name,
        "email": data.email.lower(),
        "hashed_password": hashed,
        "role": UserRole.user,
    })
    
    return user
```

## Usage in Routes

```python
# app/api/routes/users.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.repositories import UserRepository

router = APIRouter()

@router.get("/users/{id}")
def get_user(id: int, db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    user = user_repo.get(id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user
```

## Using RepositoryContainer

For cleaner dependency injection, use `RepositoryContainer`:

```python
from app.repositories import RepositoryContainer

def get_repositories(db = Depends(get_db)):
    return RepositoryContainer(db)

@router.get("/dashboard")
def dashboard(repos: RepositoryContainer = Depends(get_repositories)):
    # Access any repository through the container
    stats = {
        "total_users": repos.users.count(),
        "total_orders": repos.orders.count(),
        "menu_items": repos.menu.count(),
    }
    return stats
```

## Benefits of Repository Pattern

✅ **Separation of Concerns**: Data access logic is isolated from business logic  
✅ **Testability**: Easy to mock repositories in unit tests  
✅ **Reusability**: Common queries are defined once and reused  
✅ **Maintainability**: Changes to database queries happen in one place  
✅ **Type Safety**: Full type hints for better IDE support  

## Testing Example

```python
# tests/test_user_repository.py
def test_get_by_email():
    db = TestingSessionLocal()
    repo = UserRepository(db)
    
    # Create test user
    user = repo.create({
        "full_name": "Test User",
        "email": "test@example.com",
        "hashed_password": "hashed",
    })
    
    # Test retrieval
    found = repo.get_by_email("test@example.com")
    assert found.id == user.id
    assert found.email == "test@example.com"
```

## Migration Guide

If you're currently using direct DB queries in services, here's how to migrate:

**Before:**
```python
def get_user_orders(db, user_id):
    return db.query(Order).filter(Order.user_id == user_id).all()
```

**After:**
```python
from app.repositories import OrderRepository

def get_user_orders(db, user_id):
    order_repo = OrderRepository(db)
    return order_repo.get_user_orders(user_id)
```

## Best Practices

1. **One repository per model** - Keep each repository focused on a single entity
2. **Use base repository** - Inherit common CRUD from `BaseRepository`
3. **Name methods clearly** - Use descriptive names like `get_user_orders` not `get_orders`
4. **Return consistent types** - Always return lists or None, don't mix types
5. **Document query behavior** - Explain what filters and ordering are applied
6. **Use eager loading** - Use `joinedload()` to avoid N+1 queries for relationships

## Performance Tips

- Use indexes defined in models for frequently queried fields
- Limit result sets with `.limit()` to avoid fetching too many rows
- Use pagination (`.offset()`, `.limit()`) for large datasets
- Use `joinedload()` for related objects you know you'll need
- Consider caching for expensive queries (e.g., dashboard stats)
