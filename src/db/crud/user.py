from cgitb import reset

from sqlalchemy import select, update, insert
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models.user import User
from src.schemas.auth import UserOut
from src.security.hashing import get_password_hash


async def add_user(session: AsyncSession, email: str, first_name: str, last_name: str,
                   middle_name: str | None, password: str) -> User:
    user = User(
        email=email,
        first_name=first_name,
        last_name=last_name,
        middle_name=middle_name,
        hashed_password=get_password_hash(password),
        is_active=True
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user

async def get_user_by_email(
        session: AsyncSession,
        email: str
) -> User | None:
    result = await session.execute(select(User).where(User.email == email))

    user = result.scalar_one_or_none()

    return user

async def change_status(
        session: AsyncSession,
        email: str,
        status: bool
) -> bool:
    result = await session.execute(select(User).where(User.email == email))

    user = result.scalar_one_or_none()

    if user:
        user.is_active = status
        await session.commit()
        await session.refresh(user)
        return True

    return False




async def update_user(
    session: AsyncSession,
    email: str,
    first_name: str,
    last_name: str,
    middle_name: str | None,
    password: str
) -> User:
    """
    Обновление существующего пользователя по email.
    Возвращает обновленный ORM объект User.
    """
    result = await session.execute(
        select(User).where(User.email == email)
    )
    user = result.scalar_one()


    user.first_name = first_name
    user.last_name = last_name
    user.middle_name = middle_name
    user.hashed_password = get_password_hash(password)
    user.is_active = True

    await session.commit()
    await session.refresh(user)

    return user





