from sqlalchemy.orm import Session
from app.models.chat_model import ChatSession, ChatMessage


def create_session(db: Session, user_id: int):

    session = ChatSession(user_id=user_id)

    db.add(session)
    db.commit()
    db.refresh(session)

    return session


def save_message(db: Session, session_id: int, role: str, content: str):

    message = ChatMessage(
        session_id=session_id,
        role=role,
        content=content
    )

    db.add(message)
    db.commit()

    return message


def get_chat_history(db: Session, session_id: int):

    return db.query(ChatMessage)\
        .filter(ChatMessage.session_id == session_id)\
        .order_by(ChatMessage.created_at)\
        .all()