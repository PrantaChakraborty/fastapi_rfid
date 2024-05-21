from typing import List
import asyncio

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

from database import get_db

from .models import Rfid as RfidModel

from .schemas import CreateRfidSchema

from src.auth.models import User as AuthUserModel

from .utils import generate_email_subject_body

from config import setting


def create_rfid(message: CreateRfidSchema) -> None:
    try:
        db: Session = next(get_db())
        status = message["signal_status"]
        rfid = message["card_id"]
        rfid_obj = RfidModel(rfid=rfid,
                             status=status)
        db.add(rfid_obj)
        db.commit()
        if status:
            user_obj, _ = get_user_data_from_rfid(id=rfid_obj.id)
            if user_obj is not None:
                sub, body = generate_email_subject_body(rfid_obj)
                email = user_obj.email
                asyncio.run(send_mail(email, sub, body))
    except SQLAlchemyError as e:
        print(e)
    return None


def get_user_rfid_objects(db: Session, rfid: str) -> List[RfidModel]:
    rfid_objects = db.query(RfidModel).filter(
        RfidModel.rfid == rfid, RfidModel.status == True).order_by(
        RfidModel.created_at.desc()).all()
    return rfid_objects


def get_all_rfid_objects(db: Session) -> List[RfidModel]:
    rfid_objects = db.query(RfidModel).order_by(
        RfidModel.id.desc()).all()
    return rfid_objects


async def send_mail(recipient_email: str, subject: str, body: str) -> None:
    conf = ConnectionConfig(
        MAIL_USERNAME=setting.MAIL_USERNAME,
        MAIL_PASSWORD=setting.MAIL_PASSWORD,
        MAIL_FROM=setting.MAIL_FROM,
        MAIL_PORT=setting.MAIL_PORT,
        MAIL_SERVER=setting.MAIL_SERVER,
        USE_CREDENTIALS=True,
        VALIDATE_CERTS=True,
        MAIL_STARTTLS=True,
        MAIL_SSL_TLS=False
    )
    message = MessageSchema(
        subject=subject,
        recipients=[recipient_email],
        body=body,
        subtype="plain"
    )
    fm = FastMail(conf)
    await fm.send_message(message)


def get_user_data_from_rfid(
        id: int):
    db: Session = next(get_db())
    rfid_objects = db.query(RfidModel).filter(RfidModel.id == id).first()
    user_object = db.query(AuthUserModel).filter(AuthUserModel.rfid ==
                                                 rfid_objects.rfid).first()
    return user_object, rfid_objects

