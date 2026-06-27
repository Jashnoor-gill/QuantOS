from typing import Optional

from sqlalchemy.orm import Session

from app.modules.ai_assistant.models import AIConversation
from app.modules.ai_assistant.schemas import AIConversationCreate, AIConversationUpdate


def get_ai_conversation(db: Session, conversation_id: int) -> Optional[AIConversation]:
    return db.query(AIConversation).filter(AIConversation.id == conversation_id).first()


def list_ai_conversations(
    db: Session,
    user_id: Optional[int] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
):
    q = db.query(AIConversation)

    if user_id is not None:
        q = q.filter(AIConversation.user_id == user_id)
    if status:
        q = q.filter(AIConversation.status == status)

    return q.offset(skip).limit(limit).all()


def create_ai_conversation(db: Session, payload: AIConversationCreate) -> AIConversation:
    db_obj = AIConversation(
        user_id=payload.user_id,
        prompt=payload.prompt,
        response=payload.response,
        model_name=payload.model_name,
        token_usage=payload.token_usage,
        latency_ms=payload.latency_ms,
        status=payload.status,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_ai_conversation(
    db: Session,
    conversation_id: int,
    payload: AIConversationUpdate,
) -> Optional[AIConversation]:
    obj = get_ai_conversation(db, conversation_id)
    if obj is None:
        return None

    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(obj, k, v)

    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def delete_ai_conversation(db: Session, conversation_id: int) -> bool:
    obj = get_ai_conversation(db, conversation_id)
    if obj is None:
        return False

    db.delete(obj)
    db.commit()
    return True

