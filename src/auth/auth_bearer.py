from typing import Optional
from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.config import setting
from .exceptions import InvalidTokenError
from jose import jwt


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

    @staticmethod
    def verify_jwt(jwtoken: str) -> bool:
        try:
            payload = decode_jwt(jwtoken)
            if payload is not None:
                return True
            return False
        except jwt.ExpiredSignatureError:
            return False
        except jwt.JWTError:
            return False


jwt_bearer = JWTBearer()
