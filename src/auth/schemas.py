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
