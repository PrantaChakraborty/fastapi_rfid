from pydantic import BaseModel, field_serializer
from .models import Rfid


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

    # created_at: datetime

    @staticmethod
    def from_orm(obj: Rfid) -> "RfidSchema":
        return RfidSchema(
            id=obj.id,
            rfid=obj.rfid,
            status=obj.status,
            date=obj.created_at.date().strftime("%Y-%m-%d"),
            # Customize date format here
            time=obj.created_at.time().strftime("%H:%M"),
            # Customize time format here
        )

    class Config:
        from_attributes = True
        use_enum_values = True
