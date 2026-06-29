from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user


from app.modules.portfolio_optimizer.schemas import (
    PortfolioCreate,
    PortfolioListResponse,
    PortfolioResponse,
    PortfolioUpdate,
)
from app.modules.portfolio_optimizer.services import (
    create_portfolio,
    delete_portfolio,
    get_portfolio,
    list_portfolios,
    update_portfolio,
)

router = APIRouter()


@router.post(
    "/portfolios",
    response_model=PortfolioResponse,
    status_code=status.HTTP_201_CREATED,
)
def create(payload: PortfolioCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    try:
        return create_portfolio(db, payload)

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get(
    "/portfolios",
    response_model=PortfolioListResponse,
)
def list(
    status: Optional[str] = None,
    optimization_method: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    items = list_portfolios(
        db,
        status=status,
        optimization_method=optimization_method,
        skip=skip,
        limit=limit,
    )
    return PortfolioListResponse(items=items)


@router.get("/portfolios/{portfolio_id}", response_model=PortfolioResponse)
def get(portfolio_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    obj = get_portfolio(db, portfolio_id)
    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Portfolio not found")
    return obj



@router.put("/portfolios/{portfolio_id}", response_model=PortfolioResponse)
def update(
    portfolio_id: int,
    payload: PortfolioUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    try:
        obj = update_portfolio(db, portfolio_id, payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Portfolio not found")
    return obj


@router.delete("/portfolios/{portfolio_id}")
def delete(portfolio_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    ok = delete_portfolio(db, portfolio_id)

    if not ok:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Portfolio not found")
    return {"deleted": True}

