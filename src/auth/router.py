from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database import get_db

from .service import (get_user, create_user, create_token)
from .schemas import GetUser, CreateUser, LoginUser


from .utils import verify_pwd
from .auth_bearer import jwt_bearer

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
    if user:
        if verify_pwd(payload.password, user.hashed_password):
            token_obj = create_token(db, user.id)

            return {
                'access_token': token_obj.access_token,
                'refresh_token': token_obj.refresh_token,
                "user_type": user.role}
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail="Incorrect email or password")

# @auth_route.post("logout")
