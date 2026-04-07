"""
app/api/routes/auth.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CoalSpark Restaurant — Authentication Routes

Endpoints:
  POST /api/v1/auth/register  →  Register new user, returns JWT
  POST /api/v1/auth/login     →  Login, returns JWT
  GET  /api/v1/auth/me        →  Get current user profile
  PUT  /api/v1/auth/me        →  Update current user profile
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user import (
    UserCreate,
    UserLogin,
    UserRead,
    UserUpdate,
    Token,
)
from app.services import auth_service
from app.utils.dependencies import get_current_user
from app.models.user import User

# ── Router instance ───────────────────────────────────────────────────────────
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


# ─────────────────────────────────────────────────────────────────────────────
# POST /auth/register
# ─────────────────────────────────────────────────────────────────────────────
@router.post(
    "/register",
    response_model=Token,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new customer account",
    responses={
        201: {"description": "User registered successfully, JWT returned."},
        409: {"description": "Email already registered."},
        422: {"description": "Validation error (weak password, bad email, etc.)."},
    },
)
def register(
    data: UserCreate,
    db: Session = Depends(get_db),
):
    """
    ## Register a new user

    Creates a brand-new customer account and immediately returns a signed
    JWT access token so the client can proceed without a separate login step.

    ### Rules
    - Email must be unique across all accounts.
    - Password must be **at least 8 characters**.
    - The `role` is always set to `user` on self-registration.
      Admins must be promoted directly in the database.

    ### Flow
    ```
    Request body → Validate → Hash password → INSERT user → Sign JWT → Return Token
    ```
    """
    # 1. Create user in DB (raises 409 if email taken)
    user = auth_service.register_user(db, data)

    # 2. Generate JWT with sub=email, role claim
    token = auth_service.generate_token(user)

    # 3. Return token + user profile
    return Token(
        access_token=token,
        token_type="bearer",
        user=UserRead.model_validate(user),
    )


# ─────────────────────────────────────────────────────────────────────────────
# POST /auth/login
# ─────────────────────────────────────────────────────────────────────────────
@router.post(
    "/login",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    summary="Login and receive a JWT access token",
    responses={
        200: {"description": "Login successful, JWT returned."},
        401: {"description": "Invalid credentials or deactivated account."},
    },
)
def login(
    data: UserLogin,
    db: Session = Depends(get_db),
):
    """
    ## Login

    Authenticates with email + password.
    Returns a signed JWT access token valid for **24 hours**.

    ### Usage
    After receiving the token, attach it to every protected request:
    ```
    Authorization: Bearer <your_token_here>
    ```

    ### Flow
    ```
    Email → DB lookup → bcrypt.verify(password, hash) → Sign JWT → Return
    ```

    Raises **401** if:
    - Email is not found
    - Password does not match
    - Account has been deactivated by an admin
    """
    # 1. Verify credentials (raises 401 on failure)
    user = auth_service.authenticate_user(db, data.email, data.password)

    # 2. Sign a fresh token
    token = auth_service.generate_token(user)

    # 3. Return token + embedded user info
    return Token(
        access_token=token,
        token_type="bearer",
        user=UserRead.model_validate(user),
    )


# ─────────────────────────────────────────────────────────────────────────────
# GET /auth/me
# ─────────────────────────────────────────────────────────────────────────────
@router.get(
    "/me",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
    summary="Get the authenticated user's profile",
    responses={
        200: {"description": "User profile returned."},
        401: {"description": "Token missing, expired, or invalid."},
    },
)
def get_me(
    current_user: User = Depends(get_current_user),
):
    """
    ## Get current user

    Returns the profile of the user whose JWT token is attached to the request.

    ### How it works
    1. `get_current_user` dependency extracts the Bearer token from the header.
    2. Decodes and validates the JWT signature & expiry.
    3. Looks up the `sub` (email) claim in the `users` table.
    4. Returns the user if active, raises **401** otherwise.
    """
    return current_user


# ─────────────────────────────────────────────────────────────────────────────
# PUT /auth/me
# ─────────────────────────────────────────────────────────────────────────────
@router.put(
    "/me",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
    summary="Update current user's profile",
    responses={
        200: {"description": "Profile updated."},
        401: {"description": "Not authenticated."},
    },
)
def update_me(
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    ## Update profile

    Partial update — only fields included in the request body are modified.
    Users can update their `full_name` and `phone`.
    Email and role changes require admin action.
    """
    update_fields = data.model_dump(exclude_unset=True)

    if not update_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update.",
        )

    for field, value in update_fields.items():
        setattr(current_user, field, value)

    db.commit()
    db.refresh(current_user)
    return current_user