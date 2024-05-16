from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database import get_db
from .service import (get_user, create_user, )
from .schemas import GetUser, CreateUser, LoginUser
from datetime import date, datetime, timedelta, time
from .utils import create_access_token, create_refresh_token, verify_pwd

auth_route = APIRouter(prefix="/auth", tags=["Authentication"])


@auth_route.post("/register", response_model=GetUser)
def register_user(payload: CreateUser, db: Session = Depends(get_db)):
    if not payload.email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Please add Email",
        )
    user = get_user(db, payload.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User with email {payload.email} already exists",
        )
    user = create_user(db, payload)
    print(user)

    return user


@auth_route.post("/login")
def login_user(payload: LoginUser, db: Session = Depends(get_db)):
    """
    Login user based on email and password
    """
    if not payload.email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Please add email",
        )

    user = get_user(db, payload.email)
    if verify_pwd(payload.password, user.hashed_password):
        token = create_access_token(user.id, timedelta(minutes=30))
        refresh = create_refresh_token(user.id, timedelta(minutes=1008))

        return {'access_token': token, 'token_type': 'bearer',
                'refresh_token': refresh, "user_id": user.id}
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail="Incorrect email or password")

# @auth_route.post("logout")
