from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ResearchReportCreate(BaseModel):
    title: str
    report_type: Optional[str] = None
    content: str

    generated_by: Optional[str] = None
    status: Optional[str] = None


class ResearchReportUpdate(BaseModel):
    title: Optional[str] = None
    report_type: Optional[str] = None
    content: Optional[str] = None

    generated_by: Optional[str] = None
    status: Optional[str] = None


class ResearchReportResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int

    title: str
    report_type: Optional[str]
    content: str

    generated_by: Optional[str]
    status: Optional[str]

    created_at: datetime
    updated_at: datetime


class ResearchReportListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    items: list[ResearchReportResponse]

