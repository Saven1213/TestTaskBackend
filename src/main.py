from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.db.session import create_db
from src.routes import register_routers


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db()
    yield



app = FastAPI(
    title='Система авторизации и аунтефикации',
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins='127.0.0.1',
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_routers(app)





