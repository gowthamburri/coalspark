from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.schemas.review import ReviewCreate, ReviewRead
from app.services import review_service
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.post("/", response_model=ReviewRead)
def create_review(
    data: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return review_service.create_review(db, current_user.id, data)


@router.get("/me", response_model=list[ReviewRead])
def my_reviews(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return review_service.list_my_reviews(db, current_user.id)


@router.get("/menu-item/{menu_item_id}", response_model=list[ReviewRead])
def list_item_reviews(menu_item_id: int, db: Session = Depends(get_db)):
    return review_service.list_item_reviews(db, menu_item_id)

