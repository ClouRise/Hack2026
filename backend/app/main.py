import logging
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .routers import tests
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.auth import hash_password
from app.core.config import settings
from app.db.session import AsyncSessionLocal
from app.models.user import User as UserModel, UserRole
from app.routers import users, chat


app = FastAPI(
    title="FastAPI",
    version="0.1.1"
)

logger = logging.getLogger(__name__)


@app.on_event("startup")
async def bootstrap_admin() -> None:
    if not (settings.DEBUG and settings.BOOTSTRAP_ADMIN):
        return

    email = settings.BOOTSTRAP_ADMIN_EMAIL.strip()
    password = settings.BOOTSTRAP_ADMIN_PASSWORD
    if not email or not password:
        return

    try:
        async with AsyncSessionLocal() as db:
            result = await db.execute(
                select(UserModel).where(UserModel.role == UserRole.ADMIN)
            )
            existing_admin = result.scalar_one_or_none()
            if existing_admin:
                return

            admin = UserModel(
                email=email,
                hashed_password=hash_password(password),
                name="Admin",
                role=UserRole.ADMIN,
                is_blocked=False,
            )
            db.add(admin)
            await db.commit()

            logger.warning(
                "Bootstrap admin created: %s (password: %s)", email, password
            )
    except SQLAlchemyError as exc:
        logger.warning("Bootstrap admin skipped (db not ready): %s", exc)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       #Разрешить все домены   
    allow_credentials=True,    # Разрешить куки и авторизацию
    allow_methods=["*"],       # Разрешить все HTTP методы
    allow_headers=["*"],       # Разрешить все заголовки
    expose_headers=["*"],
)

media_dir = Path(__file__).resolve().parents[1] / "media"
app.mount("/media", StaticFiles(directory=str(media_dir)), name="media")


#ПРИЛОЖЕНИЕ FASTAPI
app.include_router(users.router)
app.include_router(chat.router)
app.include_router(tests.router)

#КОРНЕВОЙ ЭНДПОИНТ 
@app.get("/")
async def root():
    """
    КОРНЕВОЙ МАРШРУТ, ДЛЯ ПРОВЕРКИ API
    """
    return {"message": "ДОБРО ПОЖАЛОВАТЬ"}
