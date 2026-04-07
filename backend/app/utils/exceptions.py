"""
app/utils/exceptions.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CoalSpark Restaurant — Custom HTTP Exception Factories

Provides a set of factory functions that return pre-configured
FastAPI HTTPException instances with consistent error formats.

Why factory functions instead of raw HTTPException?
  1. Consistency — every 404 has the same shape and status code.
  2. Readability — `raise not_found("Menu item")` is clearer
     than `raise HTTPException(status_code=404, detail="...")`.
  3. Testability — you can mock or check these calls in unit tests.
  4. Single source of truth — if you want to change how 400 errors
     look across the whole app, change it here once.

Usage:
  from app.utils.exceptions import not_found, bad_request

  item = db.query(MenuItem).filter(MenuItem.id == id).first()
  if not item:
      raise not_found("Menu item")   # → 404 "Menu item not found."
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

from fastapi import HTTPException, status
from typing import Optional, Any, Dict


# ─────────────────────────────────────────────────────────────────────────────
# 400 Bad Request
# ─────────────────────────────────────────────────────────────────────────────
def bad_request(
    detail: str = "The request could not be processed. Please check your input.",
    headers: Optional[Dict[str, Any]] = None,
) -> HTTPException:
    """
    400 Bad Request — used when the client sends semantically invalid data
    that passes structural validation but fails business rule checks.

    Examples:
        - Uploading an unsupported file type
        - Ordering more than the maximum allowed quantity
        - Sending an empty update body
        - Trying to cancel an order that is already confirmed

    Args:
        detail  : Human-readable explanation of what went wrong.
        headers : Optional extra HTTP response headers.

    Returns:
        HTTPException with status 400.

    Usage:
        raise bad_request("File type 'image/gif' is not allowed.")
        raise bad_request("Cart cannot be empty when placing an order.")
    """
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=detail,
        headers=headers,
    )


# ─────────────────────────────────────────────────────────────────────────────
# 401 Unauthorized
# ─────────────────────────────────────────────────────────────────────────────
def unauthorized(
    detail: str = "Authentication is required. Please log in and try again.",
) -> HTTPException:
    """
    401 Unauthorized — used when a request requires authentication that is
    either missing or invalid.

    Examples:
        - Missing or expired JWT token
        - Invalid email/password on login
        - Token belongs to a deleted user

    Args:
        detail : Message explaining the auth failure (keep vague for security).

    Returns:
        HTTPException with status 401 and WWW-Authenticate header.

    Usage:
        raise unauthorized("Incorrect email or password.")
        raise unauthorized("Your session has expired. Please log in again.")

    Note:
        Always include the WWW-Authenticate header for RFC 7235 compliance.
        This tells HTTP clients how to authenticate.
    """
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


# ─────────────────────────────────────────────────────────────────────────────
# 403 Forbidden
# ─────────────────────────────────────────────────────────────────────────────
def forbidden(
    detail: str = "You do not have permission to perform this action.",
) -> HTTPException:
    """
    403 Forbidden — used when the request is authenticated but the user
    does not have sufficient privileges for the requested action.

    Examples:
        - A regular user trying to access admin endpoints
        - An admin trying to modify a protected system resource
        - A user trying to cancel another user's order

    Args:
        detail : Message explaining why access was denied.

    Returns:
        HTTPException with status 403.

    Usage:
        raise forbidden("Admin access is required.")
        raise forbidden("You can only modify your own account.")

    Note:
        Use 404 instead of 403 if you don't want to reveal whether
        a resource exists (prevents enumeration attacks on user-owned data).
    """
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=detail,
    )


# ─────────────────────────────────────────────────────────────────────────────
# 404 Not Found
# ─────────────────────────────────────────────────────────────────────────────
def not_found(
    resource: str = "Resource",
) -> HTTPException:
    """
    404 Not Found — used when the requested resource does not exist.

    This is the most commonly used exception factory in the codebase.

    Args:
        resource : Name of the resource that wasn't found.
                   Used to build a human-readable message.
                   Examples: "Menu item", "Order #42", "User #7"

    Returns:
        HTTPException with status 404.

    Usage:
        raise not_found("Menu item")       → "Menu item not found."
        raise not_found("Order #42")       → "Order #42 not found."
        raise not_found("User")            → "User not found."

    Note:
        For user-owned resources (orders, profile data), prefer raising
        not_found() even when the resource exists but belongs to another
        user. This prevents IDOR (Insecure Direct Object Reference) attacks
        where an attacker probes IDs to discover other users' data.
    """
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{resource} not found.",
    )


# ─────────────────────────────────────────────────────────────────────────────
# 409 Conflict
# ─────────────────────────────────────────────────────────────────────────────
def already_exists(
    resource: str = "Resource",
) -> HTTPException:
    """
    409 Conflict — used when a creation request would violate a uniqueness
    constraint (duplicate resource).

    Examples:
        - Registering with an email that's already taken
        - Creating a restaurant when one already exists (singleton pattern)
        - Duplicate SKU or menu item name (if uniqueness is enforced)

    Args:
        resource : Description of the duplicate entity.

    Returns:
        HTTPException with status 409.

    Usage:
        raise already_exists("An account with this email")
        raise already_exists("A restaurant record")

    Response detail format:
        "An account with this email already exists."
    """
    return HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"{resource} already exists.",
    )


# ─────────────────────────────────────────────────────────────────────────────
# 422 Unprocessable Entity
# ─────────────────────────────────────────────────────────────────────────────
def unprocessable(
    detail: str = "The submitted data could not be processed.",
) -> HTTPException:
    """
    422 Unprocessable Entity — used when the request body is syntactically
    valid (can be parsed) but semantically invalid for business logic reasons.

    Note: FastAPI automatically raises 422 for Pydantic validation failures.
    Use this factory only for custom business-logic validation that Pydantic
    cannot catch (e.g. cross-field consistency checks).

    Examples:
        - A date range where end_date < start_date
        - A discount code that is valid in format but expired
        - A cart total that doesn't match the sum of its items

    Args:
        detail : Message describing the semantic validation failure.

    Returns:
        HTTPException with status 422.

    Usage:
        raise unprocessable("The order total does not match the sum of items.")
        raise unprocessable("Check-out date must be after check-in date.")
    """
    return HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=detail,
    )


# ─────────────────────────────────────────────────────────────────────────────
# 500 Internal Server Error
# ─────────────────────────────────────────────────────────────────────────────
def server_error(
    detail: str = "An unexpected error occurred. Please try again later.",
) -> HTTPException:
    """
    500 Internal Server Error — used for unexpected failures that are not
    the client's fault.

    Examples:
        - Failed to write to disk (image upload to full disk)
        - External payment gateway is unreachable
        - Unexpected database constraint violation

    Args:
        detail : Safe-to-expose message (never include stack traces or secrets).

    Returns:
        HTTPException with status 500.

    Usage:
        raise server_error("Failed to process payment. Please try again.")
        raise server_error("Image could not be saved. Storage may be full.")

    Warning:
        Do NOT expose exception messages, stack traces, or internal paths
        in the detail field. Log the full error server-side and return only
        a generic user-facing message here.
    """
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=detail,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Convenience aliases
# ─────────────────────────────────────────────────────────────────────────────
# These aliases allow even shorter usage in service functions when the
# standard name is verbose:
#
#   from app.utils.exceptions import http400, http404
#   raise http404("Order")

http400 = bad_request
http401 = unauthorized
http403 = forbidden
http404 = not_found
http409 = already_exists
http422 = unprocessable
http500 = server_error