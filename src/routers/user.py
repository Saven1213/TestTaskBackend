from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from src.db.crud.user import get_user_by_id, update_user, delete_account_user
from src.db.session import get_db
from src.schemas.user import UserUpdateOut, UserUpdate
from src.schemas.auth import UserOut
from src.db.models.user import User
from src.security.oauth2 import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserOut)
async def read_my_profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.patch("/me", response_model=UserUpdateOut)
async def update_my_profile(
        user_data: UserUpdate,
        current_user: User = Depends(get_current_user),  # получаем текущего пользователя из токена
        db: AsyncSession = Depends(get_db)
):

    if user_data.email and user_data.email != current_user.email:
        existing = await db.execute(
            select(User).where(
                User.email == user_data.email,
                User.id != current_user.id
            )
        )
        if existing.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Пользователь с такой почтой уже существует'
            )


    updated_user = await update_user(
        session=db,
        user_id=current_user.id,
        email=user_data.email,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        middle_name=user_data.middle_name
    )

    response_data = UserUpdateOut(
        id=updated_user.id,
        email=updated_user.email,
        first_name=updated_user.first_name,
        last_name=updated_user.last_name,
        middle_name=updated_user.middle_name,
        created_at=updated_user.created_at,
        updated_at=datetime.utcnow()
    )

    return response_data

@router.post('/me/delete_account')
async def delete_account(
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    is_delete = await delete_account_user(user_id=current_user.id, session=db)

    if is_delete:
        return {'message': 'Аккаунт успешно удален'}

    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Пользователь не найден'
        )

