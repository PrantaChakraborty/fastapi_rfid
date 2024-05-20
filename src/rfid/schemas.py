from pydantic import BaseModel
from .models import Rfid

from src.auth.service import get_user_name


class CreateRfidSchema(BaseModel):
    rfid: str
    status: bool

    class Config:
        from_attributes = True
        use_enum_values = True


class RfidSchema(BaseModel):
    id: int
    rfid: str
    status: bool
    date: str
    time: str
    name: str

    # created_at: datetime

    @staticmethod
    def from_orm(obj: Rfid) -> "RfidSchema":
        user_name = get_user_name(obj.rfid)
        return RfidSchema(
            id=obj.id,
            rfid=obj.rfid,
            status=obj.status,
            date=obj.created_at.date().strftime("%Y-%m-%d"),
            # Customize date format here
            time=obj.created_at.time().strftime("%H:%M"),
            # Customize time format here
            name=user_name
        )

    class Config:
        from_attributes = True
        use_enum_values = True
