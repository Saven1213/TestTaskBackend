from fastapi import APIRouter, Depends, HTTPException, status

from src.db.crud.user import get_user_by_email, add_user
from src.db.session import get_db
from src.schemas.user import UserRegister, UserOut
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(prefix='/auth')


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register_new_user(
    user_data: UserRegister,
    db: AsyncSession = Depends(get_db)
):

    existing_user = await get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже существует"
        )


    if user_data.password != user_data.password_confirm:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пароли не совпадают"
        )

    try:
        new_user = await add_user(
            session=db,
            email=user_data.email,
            password=user_data.password,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            middle_name=user_data.middle_name,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при создании пользователя: {e}"
        )


    return new_user

