"""
app/utils/dependencies.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CoalSpark Restaurant — FastAPI Dependency Injection Utilities

This module provides reusable FastAPI dependencies that are injected
into route functions via Depends().

Dependencies defined here:
  get_current_user  →  Validates JWT Bearer token, returns User
  require_admin     →  Calls get_current_user + checks admin role

Usage in routes:
  from app.utils.dependencies import get_current_user, require_admin

  @router.get("/profile")
  def profile(user: User = Depends(get_current_user)):
      return user

  @router.delete("/menu/{id}")
  def delete_item(id: int, _admin = Depends(require_admin)):
      ...

Architecture note:
  Dependencies are the ONLY place where HTTP-level concerns (request
  headers, Bearer extraction) intersect with the service layer.
  Services themselves are dependency-free and easily unit-testable.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

from fastapi import Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app.db.session import get_db
from app.core.security import decode_access_token
from app.models.user import User, UserRole


# ─────────────────────────────────────────────────────────────────────────────
# HTTP Bearer scheme
# ─────────────────────────────────────────────────────────────────────────────
# This tells FastAPI to:
# 1. Expect an "Authorization: Bearer <token>" header.
# 2. Show a "Authorize" button in the /docs Swagger UI.
# 3. Return 403 (not 401) if no credentials are provided at all.
#
# auto_error=False means we handle the missing-token case ourselves
# with a cleaner 401 message instead of FastAPI's default 403.
bearer_scheme = HTTPBearer(auto_error=False)


# ─────────────────────────────────────────────────────────────────────────────
# get_current_user
# ─────────────────────────────────────────────────────────────────────────────
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    FastAPI dependency: Extract and validate a JWT Bearer token,
    then return the corresponding User from the database.

    This dependency is injected into any route that requires authentication.

    Flow:
    ┌─────────────────────────────────────────────────────────┐
    │ 1. Extract Bearer token from Authorization header        │
    │ 2. Check token is present (else 401)                     │
    │ 3. Decode & verify JWT signature + expiry               │
    │ 4. Extract "sub" (email) from token payload             │
    │ 5. Look up user by email in database                    │
    │ 6. Verify user exists and is_active = True              │
    │ 7. Return User ORM object                               │
    └─────────────────────────────────────────────────────────┘

    Args:
        credentials : Extracted by FastAPI's HTTPBearer from the request header.
                      None if no Authorization header was sent (auto_error=False).
        db          : Database session from get_db() dependency.

    Returns:
        User : The authenticated, active User ORM instance.

    Raises:
        HTTPException 401 :
          - Authorization header is missing entirely.
          - Token format is invalid (not a valid JWT).
          - Token signature verification fails (wrong SECRET_KEY).
          - Token has expired.
          - "sub" (email) claim is missing from the payload.
          - No user found with the email from the token payload.
        HTTPException 403 :
          - User exists but is_active = False (account deactivated by admin).

    Security considerations:
        - Tokens are signed with HS256 using settings.SECRET_KEY.
        - Expired tokens are rejected by the jose library.
        - Deactivated users are rejected even with a valid token.
        - We deliberately use the same 401 message for all token
          failures to prevent information leakage.
    """

    # ── Shared error for all token-related failures ───────────────────────────
    # Using a single message prevents attackers from distinguishing between
    # "token not present", "token expired", "token tampered", etc.
    auth_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authentication required. Please provide a valid Bearer token.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # ── Step 1 & 2: Check token is present ────────────────────────────────────
    if not credentials or not credentials.credentials:
        raise auth_error

    raw_token: str = credentials.credentials

    # ── Step 3 & 4: Decode JWT ────────────────────────────────────────────────
    # decode_access_token() verifies signature + expiry using python-jose.
    # Returns the payload dict on success, or None on any failure.
    payload = decode_access_token(raw_token)

    if payload is None:
        # Token was malformed, expired, or had an invalid signature
        raise auth_error

    # Extract the "sub" claim (user email)
    email: str = payload.get("sub")

    if not email:
        # Token is structurally valid JWT but missing the required "sub" claim
        raise auth_error

    # ── Step 5: Database lookup ───────────────────────────────────────────────
    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if not user:
        # Email in token doesn't match any user — account may have been deleted
        raise auth_error

    # ── Step 6: Active check ──────────────────────────────────────────────────
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                "Your account has been deactivated. "
                "Please contact the restaurant for assistance."
            ),
        )

    # ── Step 7: Return the verified user ──────────────────────────────────────
    return user


# ─────────────────────────────────────────────────────────────────────────────
# require_admin
# ─────────────────────────────────────────────────────────────────────────────
def require_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    FastAPI dependency: Ensures the current user has the 'admin' role.

    Builds on get_current_user — the token is validated first, then the
    role is checked. This means:
      - Missing/invalid token → 401 (from get_current_user)
      - Valid token but role = 'user' → 403 (from this function)
      - Valid token and role = 'admin' → returns User

    Usage:
        @router.delete("/menu/{id}")
        def delete_item(id: int, _admin: User = Depends(require_admin)):
            # _admin is unused because we just need the guard to run.
            # Prefix with _ to signal "intentionally unused".
            return menu_service.delete_menu_item(db, id)

    Args:
        current_user : Injected by get_current_user — already validated.

    Returns:
        User : The authenticated admin User ORM instance.

    Raises:
        HTTPException 403 : If the user's role is not 'admin'.

    Note:
        The returned User object is available in routes if you need
        the admin's identity (e.g. for audit logs). If you only need
        the guard and not the user, name the parameter with a _ prefix.
    """
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                "Admin access is required to perform this action. "
                "If you believe this is an error, contact the system administrator."
            ),
        )

    return current_user


# ─────────────────────────────────────────────────────────────────────────────
# get_optional_user  (bonus — for routes that work for both anon + authed)
# ─────────────────────────────────────────────────────────────────────────────
def get_optional_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> Optional[User]:
    """
    FastAPI dependency: Returns the authenticated User if a valid token
    is present, or None if no token is provided.

    Unlike get_current_user, this does NOT raise 401 on missing token.
    Use this for routes that have optional authentication — e.g. a menu
    endpoint that shows extra info to logged-in users but still works
    for anonymous visitors.

    Args:
        credentials : Optional Bearer token from request header.
        db          : DB session.

    Returns:
        User | None : Authenticated User, or None if no/invalid token.

    Example:
        @router.get("/menu/")
        def menu(user: User | None = Depends(get_optional_user)):
            items = menu_service.get_all_menu_items(db)
            if user:
                # personalise response for logged-in users
                ...
            return items
    """
    if not credentials or not credentials.credentials:
        return None

    payload = decode_access_token(credentials.credentials)
    if not payload:
        return None

    email = payload.get("sub")
    if not email:
        return None

    user = db.query(User).filter(User.email == email).first()

    if not user or not user.is_active:
        return None

    return user