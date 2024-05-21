from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from database import get_db

from .service import (get_user, create_user, create_token, get_users,
                      get_user_token)
from .schemas import (
    GetUser,
    CreateUser,
    LoginUser,
    GetUserSchema,
    RefreshTokenSchema,
    TokenSchema
)

from .auth_bearer import jwt_bearer, decode_jwt
from .utils import verify_pwd

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
                "user_type": user.role,
                "rfid": user.rfid}
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail="Incorrect email or password")


# @auth_route.post("logout")
@auth_route.get("/home",
                dependencies=[Depends(jwt_bearer)])
def get_home(db: Session = Depends(get_db)) -> List[GetUserSchema]:
    user = get_users(db)
    return user


@auth_route.post('/logout')
def logout(dependencies=Depends(jwt_bearer), db: Session = Depends(get_db)) \
        -> Response:
    token = dependencies
    payload = decode_jwt(token)
    user_id = payload['sub']
    user_token = get_user_token(db, user_id, access_token=token)

    if user_token:
        user_token.status = False
        db.add(user_token)
        db.commit()

    return Response(status_code=status.HTTP_200_OK, content="User logged out")


@auth_route.post('/token_refresh', response_model=TokenSchema)
def token_refresh(payload: RefreshTokenSchema, db: Session = Depends(get_db)
                  ) -> Any:
    existing_token = get_user_token(db=db,
                                    refresh_token=payload.refresh_token)
    if not existing_token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid token")
    user_id = existing_token.user_id
    existing_token.status = False
    db.add(existing_token)
    db.commit()
    new_token = create_token(db, user_id)
    return {"access_token": new_token.access_token,
            "refresh_token": new_token.refresh_token}
