from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from datetime import datetime

from app.database.database import Base


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    title = Column(String, default="New Chat")
    created_at = Column(DateTime, default=datetime.utcnow)


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)

    session_id = Column(Integer, ForeignKey("chat_sessions.id"))

    role = Column(String)  # "user" or "assistant"

    content = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)