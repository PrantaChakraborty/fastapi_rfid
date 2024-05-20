from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from database import get_db

from src.auth.auth_bearer import jwt_bearer, decode_jwt
from src.auth.service import get_user_rfid_card_no

from .schemas import (
    RfidSchema
)

from .service import get_user_rfid_objects

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
