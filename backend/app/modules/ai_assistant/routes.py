from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user

from app.modules.ai_assistant.schemas import (
    AIConversationCreate,
    AIConversationListResponse,
    AIConversationResponse,
    AIConversationUpdate,
)
from app.modules.ai_assistant.services import (
    create_ai_conversation,
    delete_ai_conversation,
    get_ai_conversation,
    list_ai_conversations,
    update_ai_conversation,
)

router = APIRouter()


@router.post(
    "/ai-conversations",
    response_model=AIConversationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create(payload: AIConversationCreate, db: Session = Depends(get_db)):
    return create_ai_conversation(db, payload)


@router.get(
    "/ai-conversations",
    response_model=AIConversationListResponse,
)
def list(
    user_id: Optional[int] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    items = list_ai_conversations(db, user_id=user_id, status=status, skip=skip, limit=limit)
    return AIConversationListResponse(items=items)


@router.get("/ai-conversations/{conversation_id}", response_model=AIConversationResponse)
def get(conversation_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):

    obj = get_ai_conversation(db, conversation_id)

    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")
    return obj


@router.put("/ai-conversations/{conversation_id}", response_model=AIConversationResponse)
def update(
    conversation_id: int,
    payload: AIConversationUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    obj = update_ai_conversation(db, conversation_id, payload)
    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")
    return obj


@router.delete("/ai-conversations/{conversation_id}")
def delete(conversation_id: int, db: Session = Depends(get_db)):
    ok = delete_ai_conversation(db, conversation_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")
    return {"deleted": True}

