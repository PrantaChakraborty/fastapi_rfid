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
