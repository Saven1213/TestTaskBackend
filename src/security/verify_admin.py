from fastapi import Depends, HTTPException, status
from src.db.models.user import User
from src.security.oauth2 import get_current_user

def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """
    Проверяет, что текущий пользователь является администратором.
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Только администраторы имеют доступ"
        )
    return current_user