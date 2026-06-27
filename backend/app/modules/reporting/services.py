from typing import Optional

from sqlalchemy.orm import Session

from app.modules.reporting.models import ResearchReport
from app.modules.reporting.schemas import (
    ResearchReportCreate,
    ResearchReportUpdate,
)


def get_research_report(db: Session, report_id: int) -> Optional[ResearchReport]:
    return db.query(ResearchReport).filter(ResearchReport.id == report_id).first()


def list_research_reports(
    db: Session,
    status: Optional[str] = None,
    report_type: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
):
    q = db.query(ResearchReport)
    if status:
        q = q.filter(ResearchReport.status == status)
    if report_type:
        q = q.filter(ResearchReport.report_type == report_type)
    return q.offset(skip).limit(limit).all()


def create_research_report(db: Session, payload: ResearchReportCreate) -> ResearchReport:
    db_obj = ResearchReport(
        title=payload.title,
        report_type=payload.report_type,
        content=payload.content,
        generated_by=payload.generated_by,
        status=payload.status,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_research_report(
    db: Session,
    report_id: int,
    payload: ResearchReportUpdate,
) -> Optional[ResearchReport]:
    obj = get_research_report(db, report_id)
    if obj is None:
        return None

    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(obj, k, v)

    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def delete_research_report(db: Session, report_id: int) -> bool:
    obj = get_research_report(db, report_id)
    if obj is None:
        return False

    db.delete(obj)
    db.commit()
    return True

