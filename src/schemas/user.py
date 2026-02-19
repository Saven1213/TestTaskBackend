from datetime import datetime

from pydantic import BaseModel, EmailStr
from typing import Optional

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    email: Optional[EmailStr] = None

    class Config:
        from_attributes = True


class UserUpdateOut(BaseModel):
    id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    email: EmailStr
    updated_at: datetime

    class Config:
        from_attributes = True