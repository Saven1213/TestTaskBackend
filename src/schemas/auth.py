

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime



class UserRegister(BaseModel):
    first_name: str = Field(min_length=2, max_length=30, description='Имя')
    last_name: str = Field(min_length=1, max_length=100, description="Фамилия")
    middle_name: str | None = Field(max_length=100, description="Отчество")
    email: EmailStr = Field(description="Email")
    password: str = Field(min_length=8, description="Пароль")
    password_confirm: str = Field(min_length=8, description="Повтор пароля")

class UserOut(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    middle_name: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
        exclude = {"hashed_password"}

class Token(BaseModel):
    token_type: str
    access_token: str
    refresh_token: str



