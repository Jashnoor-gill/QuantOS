from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user, create_access_token, create_refresh_token
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

    from passlib.context import CryptContext

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = pwd_context.hash(user.password)

    return create_user(db, user, hashed_password)



@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    existing = get_user_by_email(db, user.email)

    if existing is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    from passlib.context import CryptContext
    from app.core.security import create_access_token, create_refresh_token
    from datetime import timedelta

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    if not pwd_context.verify(user.password, existing.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    # JWT access + refresh tokens
    access_token = create_access_token({"sub": existing.username})
    refresh_token = create_refresh_token({"sub": existing.username})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token,
    }



@router.get("/me")
def me(current_user: str = Depends(get_current_user)):
    return {
        "message": "Authenticated user endpoint",
        "user": current_user,
    }

