import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean

from database import Base


class Rfid(Base):
    __tablename__ = 'rfid'
    id = Column(Integer, primary_key=True)
    rfid = Column(String)
    status = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
