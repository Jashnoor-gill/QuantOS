from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.reporting.schemas import (
    ResearchReportCreate,
    ResearchReportListResponse,
    ResearchReportResponse,
    ResearchReportUpdate,
)
from app.modules.reporting.services import (
    create_research_report,
    delete_research_report,
    get_research_report,
    list_research_reports,
    update_research_report,
)

router = APIRouter()


@router.post(
    "/research-reports",
    response_model=ResearchReportResponse,
    status_code=status.HTTP_201_CREATED,
)
def create(payload: ResearchReportCreate, db: Session = Depends(get_db)):
    return create_research_report(db, payload)


@router.get(
    "/research-reports",
    response_model=ResearchReportListResponse,
)
def list(
    status: Optional[str] = None,
    report_type: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    items = list_research_reports(
        db,
        status=status,
        report_type=report_type,
        skip=skip,
        limit=limit,
    )
    return ResearchReportListResponse(items=items)


@router.get("/research-reports/{report_id}", response_model=ResearchReportResponse)
def get(report_id: int, db: Session = Depends(get_db)):
    obj = get_research_report(db, report_id)
    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Research report not found")
    return obj


@router.put("/research-reports/{report_id}", response_model=ResearchReportResponse)
def update(
    report_id: int,
    payload: ResearchReportUpdate,
    db: Session = Depends(get_db),
):
    obj = update_research_report(db, report_id, payload)
    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Research report not found")
    return obj


@router.delete("/research-reports/{report_id}")
def delete(report_id: int, db: Session = Depends(get_db)):
    ok = delete_research_report(db, report_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Research report not found")
    return {"deleted": True}

