from typing import List

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from database import get_db

from .models import Rfid as RfidModel

from .schemas import CreateRfidSchema


def create_rfid(message: CreateRfidSchema) -> None:
    try:
        db: Session = next(get_db())
        rfid_obj = RfidModel(rfid=message["card_id"],
                             status=message["signal_status"])
        db.add(rfid_obj)
        db.commit()
    except SQLAlchemyError as e:
        print(e)
    return None


def get_user_rfid_objects(db: Session, rfid: str) -> List[RfidModel]:
    rfid_objects = db.query(RfidModel).filter(
        RfidModel.rfid ==rfid, RfidModel.status == True).order_by(
        RfidModel.created_at.desc()).all()
    return rfid_objects
