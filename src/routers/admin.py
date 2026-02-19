from datetime import datetime
from http.client import HTTPException
from sqlalchemy import select


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.crud.user import get_users, get_user_by_id, update_user
from src.db.models.user import User
from src.db.session import get_db
from src.schemas.admin import UserUpdate, UserUpdateOut
from src.security.verify_admin import require_admin

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/users")
async def get_all_users(admin: User = Depends(require_admin), db: AsyncSession = Depends(get_db)):

    users = await get_users(db)

    return {
        "message": f"Привет, админ {admin.email}!",
        "users": [
            {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "is_active": user.is_active,
                "created_at": user.created_at.isoformat() if user.created_at else None,
                "is_admin": user.is_admin
            }
            for user in users
        ]
    }

@router.patch('/users/{user_id}', response_model=UserUpdateOut)
async def update_user_by_admin(
        user_id: int,
        user_data: UserUpdate,
        db: AsyncSession = Depends(get_db),
        admin: User = Depends(require_admin)
):
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Такого пользователя нет в базе'
        )

    if user_data.email and user_data.email != user.email:
        existing_user = await db.execute(
            select(User).where(
                User.email == user_data.email,
                User.id != user_id
            )
        )
        if existing_user.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Пользователь с такой почтой уже существует'
            )


    updated_user = await update_user(
        session=db,
        email=user_data.email,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        middle_name=user_data.middle_name,
        is_admin=user_data.is_admin
    )

    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ошибка при обновлении пользователя'
        )

    new_data = UserUpdateOut(
        id=updated_user.id,
        email=updated_user.email,
        first_name=updated_user.first_name,
        last_name=updated_user.last_name,
        middle_name=updated_user.middle_name,
        is_active=updated_user.is_active,
        created_at=updated_user.created_at,
        updated_at=datetime.utcnow(),
        is_admin=updated_user.is_admin
    )

    return new_data

