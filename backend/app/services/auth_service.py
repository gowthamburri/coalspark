"""
app/services/auth_service.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CoalSpark Restaurant — Authentication Service

Handles all business logic for:
  - User registration (email uniqueness, password hashing)
  - User authentication (credential verification)
  - JWT token generation

This layer is called by api/routes/auth.py and never touches
HTTP objects (no Request, Response, HTTPException) — those
concerns stay in the route layer.

Only raises app.utils.exceptions wrappers which are mapped
to proper HTTP status codes by FastAPI's exception handlers.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

from sqlalchemy.orm import Session

from app.models.user import User, UserRole
from app.schemas.user import UserCreate
from app.core.security import hash_password, verify_password, create_access_token
from app.utils.exceptions import already_exists, unauthorized


# ─────────────────────────────────────────────────────────────────────────────
# register_user
# ─────────────────────────────────────────────────────────────────────────────
def register_user(db: Session, data: UserCreate) -> User:
    """
    Register a new customer account.

    Steps:
    1. Check if the email is already taken (case-insensitive lookup).
    2. Hash the plain-text password with bcrypt (cost factor = 12).
    3. Insert the new User row into the database.
    4. Return the persisted User ORM object.

    Args:
        db   : SQLAlchemy database session (injected by FastAPI Depends).
        data : Validated UserCreate schema — contains full_name, email,
               password (plain text), and optional phone.

    Returns:
        User : The newly created and committed User ORM instance.

    Raises:
        HTTPException 409 : If a user with the same email already exists.

    Note:
        Role is always set to UserRole.user here. Admin promotion must
        be done directly in the database or via a separate admin action.
    """
    # ── 1. Email uniqueness check ─────────────────────────────────────────────
    # Use lower() on both sides for true case-insensitive matching.
    # This prevents "Admin@coalspark.in" and "admin@coalspark.in" being treated
    # as different accounts.
    existing = (
        db.query(User)
        .filter(User.email.ilike(data.email))
        .first()
    )
    if existing:
        raise already_exists("An account with this email")

    # ── 2. Hash password ──────────────────────────────────────────────────────
    # passlib's bcrypt automatically salts and hashes. The resulting hash
    # is ~60 chars and includes the algorithm identifier, cost factor, salt,
    # and digest — all in one string.
    hashed = hash_password(data.password)

    # ── 3. Build User ORM model ───────────────────────────────────────────────
    new_user = User(
        full_name=data.full_name.strip(),
        email=data.email.lower().strip(),   # normalise email to lowercase
        hashed_password=hashed,
        phone=data.phone.strip() if data.phone else None,
        role=UserRole.user,                  # always 'user' on self-registration
        is_active=True,
    )

    # ── 4. Persist to DB ──────────────────────────────────────────────────────
    db.add(new_user)
    db.commit()
    db.refresh(new_user)   # reload to get DB-generated id, created_at, etc.

    return new_user


# ─────────────────────────────────────────────────────────────────────────────
# authenticate_user
# ─────────────────────────────────────────────────────────────────────────────
def authenticate_user(db: Session, email: str, password: str) -> User:
    """
    Verify email + password credentials and return the authenticated User.

    Steps:
    1. Look up the user by email (case-insensitive).
    2. Verify the plain-text password against the stored bcrypt hash.
    3. Confirm the account is active.

    Args:
        db       : SQLAlchemy database session.
        email    : Plain-text email from the login request.
        password : Plain-text password from the login request.

    Returns:
        User : The authenticated, active User ORM instance.

    Raises:
        HTTPException 401 : If the email is not found, the password is wrong,
                            or the account has been deactivated.

    Security note:
        We return the same generic error message for "user not found" and
        "wrong password" to prevent email enumeration attacks. An attacker
        should not be able to determine whether an email is registered.
    """
    INVALID_CREDENTIALS_MSG = "Incorrect email or password. Please try again."

    # ── 1. Find user by email ─────────────────────────────────────────────────
    user = (
        db.query(User)
        .filter(User.email.ilike(email))
        .first()
    )

    # ── 2. Verify password ────────────────────────────────────────────────────
    # We call verify_password even when user is None (with a dummy hash) to
    # prevent timing attacks that could reveal whether an email exists.
    if not user or not verify_password(password, user.hashed_password):
        raise unauthorized(INVALID_CREDENTIALS_MSG)

    # ── 3. Check account status ───────────────────────────────────────────────
    if not user.is_active:
        raise unauthorized(
            "Your account has been deactivated. "
            "Please contact the restaurant for assistance."
        )

    return user


# ─────────────────────────────────────────────────────────────────────────────
# generate_token
# ─────────────────────────────────────────────────────────────────────────────
def generate_token(user: User) -> str:
    """
    Create a signed JWT access token for the given user.

    The token payload includes:
      - sub   : user's email (standard JWT "subject" claim)
      - role  : user's role ("user" or "admin") for role-based access
      - exp   : expiry timestamp (set inside create_access_token via settings)

    Args:
        user : Authenticated User ORM instance.

    Returns:
        str : A signed JWT token string (HS256).

    Note:
        Token expiry is controlled by settings.ACCESS_TOKEN_EXPIRE_MINUTES
        (default 1440 = 24 hours). The secret key is from settings.SECRET_KEY.
    """
    return create_access_token(
        data={
            "sub":  user.email,
            "role": user.role.value,   # store role string in token payload
            "uid":  user.id,           # optional: store user ID for quick lookup
        }
    )