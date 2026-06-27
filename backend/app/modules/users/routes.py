from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.users.schemas import (
    UserCreate,
    UserLogin,
    UserResponse,
    TokenResponse,
)
from app.modules.users.services import (
    create_user,
    get_user_by_email,
)

router = APIRouter()


@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = get_user_by_email(db, user.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Replace with real password hashing later
    hashed_password = user.password

    return create_user(db, user, hashed_password)


@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    existing = get_user_by_email(db, user.email)

    if existing is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    # Replace with JWT generation later
    return {
        "access_token": "development-token",
        "token_type": "bearer",
    }


@router.get("/me")
def me():
    return {
        "message": "Authenticated user endpoint"
    }