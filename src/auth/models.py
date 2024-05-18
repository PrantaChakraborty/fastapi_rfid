import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class Token(Base):
    """
    models for token
    """
    __tablename__ = "tokens"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    access_token = Column(String(450), index=True)
    refresh_token = Column(String(450), nullable=False, index=True)
    status = Column(Boolean)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

