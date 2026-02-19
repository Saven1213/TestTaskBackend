from fastapi import FastAPI

from src.routers.auth import router as auth_router
from src.routers.user import router as user_router
from src.routers.admin import router as admin_router
from src.routers.store import router as store_router


def register_routers(app: FastAPI) -> None:
    app.include_router(auth_router)
    app.include_router(user_router)
    app.include_router(store_router)
    app.include_router(admin_router)