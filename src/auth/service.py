from sqlalchemy.orm import Session
from .models import User

from pydantic import EmailStr

from .schemas import CreateUser
from .utils import secure_pwd


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

# def get_token(db: Session, token: str):
#     return db.query(models.Token).filter(models.Token.token == token).first()
#
# def create_token(db: Session, token: str, user_id: int):
#     db_token = models.Token(token=token, user_id=user_id)
#     db.add(db_token)
#     db.commit()
#     db.refresh(db_token)
#     return db_token
