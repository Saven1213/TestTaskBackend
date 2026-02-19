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
        email: str | None = None,
        user_id: int | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
        middle_name: str | None = None,
        password: str | None = None,
        is_active: bool | None = None,
        is_admin: bool | None = None
) -> User | None:


    if not email and not user_id:
        raise ValueError("Необходимо передать email или user_id для поиска пользователя")


    query = select(User)
    if user_id is not None:
        query = query.where(User.id == user_id)
    else:
        query = query.where(User.email == email)

    result = await session.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        return None


    if first_name is not None:
        user.first_name = first_name

    if last_name is not None:
        user.last_name = last_name

    if middle_name is not None:
        user.middle_name = middle_name

    if password is not None:
        user.hashed_password = get_password_hash(password)

    if is_active is not None:
        user.is_active = is_active

    if is_admin is not None:
        user.is_admin = is_admin

    await session.commit()
    await session.refresh(user)

    return user

async def get_users(session: AsyncSession) -> list | None:
    result = await session.execute(select(User))
    users = result.scalars().all()

    if users:
        return list(users)
    else:
        return None

async def get_user_by_id(
        session: AsyncSession,
        id_: int
) -> User | None:
    result = await session.execute(select(User).where(User.id == id_))

    user = result.scalar_one_or_none()

    return user








