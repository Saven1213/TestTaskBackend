from datetime import timedelta, datetime

from dns.dnssecalgs import algorithms
from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.util import await_fallback

from jose import jwt, JWTError

from src.config import settings
from src.db.crud.user import get_user_by_email, add_user, update_user, change_status
from src.db.session import get_db
from src.schemas.auth import UserRegister, UserOut, Token
from sqlalchemy.ext.asyncio import AsyncSession

from src.security.hashing import verify_password
from src.security.jwt import create_access_token, create_refresh_token

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register_new_user(
    user_data: UserRegister,
    db: AsyncSession = Depends(get_db)
):

    existing_user = await get_user_by_email(db, user_data.email)

    if existing_user and existing_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже существует и активен"
        )


    if user_data.password != user_data.password_confirm:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пароли не совпадают"
        )





    common_data = {
        "email": user_data.email,
        "first_name": user_data.first_name,
        "last_name": user_data.last_name,
        "middle_name": user_data.middle_name,
        "password": user_data.password
    }

    try:
        if not existing_user:

            new_user = await add_user(
                session=db,
                **common_data
            )
            return UserOut.model_validate(new_user)

        else:

            updated_user = await update_user(
                session=db,
                **common_data
            )


            return UserOut.model_validate(updated_user)

    except IntegrityError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email уже занят (возможно, конфликт в базе)\n\n{e.orig}"
        )
    except Exception as e:
        await db.rollback()
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при регистрации: {str(e)}"
        )


@router.post('/login', response_model=Token)
async def login(
        form_data = Depends(OAuth2PasswordRequestForm),
        db: AsyncSession = Depends(get_db)
):
    user = await get_user_by_email(db, form_data.username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден",
            headers={"WWW-Authenticate": "Bearer"},
        )

    is_verified = verify_password(form_data.password, user.hashed_password)

    if not is_verified:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Аккаунт деактивирован или удален"
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': user.email},
        expires_delta=access_token_expires
    )

    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = create_refresh_token(
        data={'sub': user.email},
        expires_delta = refresh_token_expires
    )

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type='bearer'
    )

@router.post('/refresh', response_model=Token)
async def refresh_access_token(
        refresh_token: str = Body(...),
        db: AsyncSession = Depends(get_db)
):
    creds_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Неверный или истекший refresh токен'
    )

    try:
        payload = jwt.decode(
            refresh_token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get('sub')
        if email is None:
            raise creds_exception
    except JWTError:
        raise creds_exception

    user = await get_user_by_email(db, email)
    if not user or not user.is_active:
        raise creds_exception

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    new_access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )

    return Token(
        access_token=new_access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


@router.post('/logout')
async def logout():
    """Чтобы выйти в swagger нужно очистить токен из заголовков (вручную), а так это делается на фронте"""

    return {'message': 'Вы вышли из системы'}







