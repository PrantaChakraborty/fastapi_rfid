from sqlalchemy.orm import Session
from .models import User, Token

from pydantic import EmailStr

from .schemas import CreateUser
from .utils import secure_pwd, create_access_token, create_refresh_token


def get_user(db: Session, email: EmailStr):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: CreateUser):
    hashed_password = secure_pwd(user.password)
    db_user = User(email=user.email, name=user.name,
                   hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_token(db: Session, token: str):
    return db.query(Token).filter(Token.access_token == token).first()


def create_token(db: Session, user_id: int):
    access_token = create_access_token(user_id)
    refresh_token = create_refresh_token(user_id)
    token_obj = Token(user_id=user_id, access_token=access_token,
                      refresh_token=refresh_token, status=True)
    db.add(token_obj)
    db.commit()
    db.refresh(token_obj)
    return token_obj


def get_users(db: Session):
    return db.query(User).all()


def get_user_token(db: Session, user_id: int, access_token: str):
    tokens = db.query(Token).filter(Token.user_id == user_id,
                                    Token.access_token == access_token).first()
    return tokens
