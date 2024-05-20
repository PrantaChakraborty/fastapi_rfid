from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db

from src.auth.auth_bearer import jwt_bearer, decode_jwt
from src.auth.service import get_user_rfid_card_no

from .utils import generate_email_subject_body

from .schemas import (
    RfidSchema
)

from .service import (
    get_user_rfid_objects,
    get_all_rfid_objects,
    send_mail,
    get_user_data_from_rfid
)

rfid_route = APIRouter(prefix="/rfid", tags=["rfid"])


@rfid_route.get('/user', response_model=List[RfidSchema])
def get_user_rfid(dependencies=Depends(jwt_bearer), db: Session = Depends(
    get_db)):
    token = dependencies

    payload = decode_jwt(token)
    user_id = payload['sub']
    user_rfid_num = get_user_rfid_card_no(db, user_id)
    user_rfid = get_user_rfid_objects(db, user_rfid_num)
    r = [RfidSchema.from_orm(rfid_object) for rfid_object in user_rfid]
    return r


@rfid_route.get('/all', response_model=List[RfidSchema],
                dependencies=[Depends(jwt_bearer)])
def get_all_rfid(db: Session = Depends(
    get_db)):
    user_rfid = get_all_rfid_objects(db)
    r = [RfidSchema.from_orm(rfid_object) for rfid_object in user_rfid]
    return r


@rfid_route.post('/send_mail/{id:int}',
                 dependencies=[Depends(jwt_bearer)])
async def send_email_mail(id: int, db: Session = Depends(get_db)):
    user_obj, rfid_obj = get_user_data_from_rfid(id)
    sub, body = generate_email_subject_body(rfid_obj)
    email = user_obj.email
    await send_mail(email, sub, body)
    return {"message": "Email sent!"}
