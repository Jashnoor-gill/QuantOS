from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class AIConversationCreate(BaseModel):
    user_id: int
    prompt: str
    response: str

    model_name: Optional[str] = None
    token_usage: Optional[int] = None
    latency_ms: Optional[float] = None
    status: Optional[str] = None


class AIConversationUpdate(BaseModel):
    user_id: Optional[int] = None
    prompt: Optional[str] = None
    response: Optional[str] = None

    model_name: Optional[str] = None
    token_usage: Optional[int] = None
    latency_ms: Optional[float] = None
    status: Optional[str] = None


class AIConversationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    prompt: str
    response: str

    model_name: Optional[str]
    token_usage: Optional[int]
    latency_ms: Optional[float]
    status: Optional[str]

    created_at: datetime


class AIConversationListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    items: list[AIConversationResponse]

