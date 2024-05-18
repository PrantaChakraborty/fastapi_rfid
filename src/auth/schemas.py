from datetime import datetime

from pydantic import BaseModel, EmailStr


class GetUser(BaseModel):
    email: EmailStr
    role: str

    class Config:
        from_attributes = True
        use_enum_values = True


class LoginUser(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True
        use_enum_values = True


class CreateUser(BaseModel):
    email: EmailStr
    password: str
    name: str

    class Config:
        from_attributes = True
        use_enum_values = True


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class TokenCreateSchema(BaseModel):
    user_id: int
    access_token: str
    refresh_token: str
    status: bool
    created_at: datetime
