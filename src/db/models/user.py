

from sqlalchemy import Integer, Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from src.db.models.base import Base

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    first_name: Mapped[str] = mapped_column(String)

    last_name: Mapped[str] = mapped_column(String)

    middle_name: Mapped[str] = mapped_column(String)

    email: Mapped[str] = mapped_column(String)

    hashed_password: Mapped[str] = mapped_column(String)

    is_active: Mapped[bool] = mapped_column(Boolean)



