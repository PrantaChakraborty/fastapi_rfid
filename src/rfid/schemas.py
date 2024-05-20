from pydantic import BaseModel


class CreateRfidSchema(BaseModel):
    rfid: str
    status: bool

    class Config:
        from_attributes = True
        use_enum_values = True
