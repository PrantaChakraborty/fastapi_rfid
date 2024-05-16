from datetime import datetime, timedelta
from typing import Union, Any, Optional

from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from passlib.context import CryptContext
from jose import jwt

from .models import *
from src.config import setting
from .exceptions import InvalidTokenError


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def secure_pwd(raw_password):
    hashed = pwd_context.hash(raw_password)
    return hashed


def verify_pwd(plain, hash_passwd):
    return pwd_context.verify(plain, hash_passwd)


def create_access_token(subject: Union[str, Any],
                        expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=setting.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, setting.secret_key, setting.algorithm)
    return encoded_jwt


def create_refresh_token(subject: Union[str, Any],
                         expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=setting.REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, setting.refresh_secret_key,
                             setting.algorithm)
    return encoded_jwt


def decode_jwt(jwtoken: str):
    try:
        payload = jwt.decode(jwtoken, setting.secret_key, setting.algorithm)
        return payload
    except InvalidTokenError:
        return None


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer,
                                                                self).__call__(
            request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403,
                                    detail="Invalid authentication scheme.")
            token = credentials.credentials
            if not self.verify_jwt(token):
                raise HTTPException(status_code=403,
                                    detail="Invalid token or expired token.")
            return token
        else:
            raise HTTPException(status_code=403,
                                detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        try:
            payload = decode_jwt(jwtoken)
            if payload is not None:
                return True
            return False
        except jwt.ExpiredSignatureError:
            return False
        except jwt.JWTError:
            return False

# jwt_bearer = JWTBearer()
