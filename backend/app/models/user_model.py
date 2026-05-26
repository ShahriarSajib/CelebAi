from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime

from app.database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String, unique=True, nullable=False)

    email = Column(String, unique=True, nullable=False)

    password = Column(String, nullable=False)

    is_verified = Column(Boolean, default=False)

    profile_image = Column(String, nullable=True)

    bio = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)