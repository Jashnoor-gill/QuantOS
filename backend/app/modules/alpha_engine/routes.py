from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.alpha_engine.schemas import (
    AlphaCreate,
    AlphaListResponse,
    AlphaResponse,
    AlphaUpdate,
)
from app.modules.alpha_engine.services import (
    create_alpha,
    delete_alpha,
    get_alpha,
    list_alphas,
    update_alpha,
)

router = APIRouter()


@router.post(
    "/alphas",
    response_model=AlphaResponse,
    status_code=status.HTTP_201_CREATED,
)
def create(payload: AlphaCreate, db: Session = Depends(get_db)):
    return create_alpha(db, payload)


@router.get(
    "/alphas",
    response_model=AlphaListResponse,
)
def list(
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    items = list_alphas(db, status=status, skip=skip, limit=limit)
    return AlphaListResponse(items=items)


@router.get("/alphas/{alpha_id}", response_model=AlphaResponse)
def get(alpha_id: int, db: Session = Depends(get_db)):
    obj = get_alpha(db, alpha_id)
    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alpha not found")
    return obj


@router.put("/alphas/{alpha_id}", response_model=AlphaResponse)
def update(
    alpha_id: int,
    payload: AlphaUpdate,
    db: Session = Depends(get_db),
):
    obj = update_alpha(db, alpha_id, payload)
    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alpha not found")
    return obj


@router.delete("/alphas/{alpha_id}")
def delete(alpha_id: int, db: Session = Depends(get_db)):
    ok = delete_alpha(db, alpha_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alpha not found")
    return {"deleted": True}

