import datetime
from typing import Union, Any, Optional

from fastapi.security import OAuth2PasswordBearer

from passlib.context import CryptContext
from jose import jwt

from .models import *
from src.config import setting

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def secure_pwd(raw_password):
    hashed = pwd_context.hash(raw_password)
    return hashed


def verify_pwd(plain, hash_passwd):
    return pwd_context.verify(plain, hash_passwd)


def create_access_token(subject: Union[str, Any]) -> str:

    expires_delta = datetime.datetime.utcnow() + datetime.timedelta(
            minutes=setting.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, setting.secret_key, setting.algorithm)
    return encoded_jwt


def create_refresh_token(subject: Union[str, Any]) -> str:

    expires_delta = datetime.datetime.utcnow() + datetime.timedelta(
            minutes=setting.REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, setting.refresh_secret_key,
                             setting.algorithm)
    return encoded_jwt

