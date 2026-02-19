from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models.user import User
from src.schemas.user import UserOut
from src.security.hashing import get_password_hash


async def add_user(
        session: AsyncSession,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        middle_name: str | None
) -> User:
    hashed_password = get_password_hash(password)

    user = User(
        email=email,
        hashed_password=hashed_password,
        first_name=first_name,
        last_name=last_name,
        middle_name=middle_name,
        is_active=True
    )

    session.add(user)

    await session.commit()

    return user

async def get_user_by_email(
        session: AsyncSession,
        email: str
) -> User | None:
    result = await session.execute(select(User).where(User.email == email))

    user = result.scalar_one_or_none()

    return user



