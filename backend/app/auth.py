import secrets
import hashlib
import string
import uuid

import jwt
from typing import Optional
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status,Request, Cookie
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.refresh_token import Token as RefreshToken
from app.models.user import User as UserModel
from app.core.config import settings
from app.db.session import get_db

# Контекст для хеширования паролей
pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")


# ==================== ГЕНЕРАЦИЯ ПАРОЛЯ ====================

def generate_password(length: int = 12) -> str:
    """Генерация случайного пароля"""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return password


# ==================== ПАРОЛИ ====================

def hash_password(password: str) -> str:
    """Хеширование пароля"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверка пароля"""
    return pwd_context.verify(plain_password, hashed_password)


# ==================== ACCESS TOKEN ====================

def create_access_token(data: dict) -> str:
    """Создание JWT Access Token"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_ACCESS_EXPIRE_MINUT)
    to_encode.update({"exp": expire})
    secret_key = settings.JWT_SECRET_KEY or settings.SECRET_KEY
    return jwt.encode(to_encode, secret_key, algorithm=settings.JWT_ALGORITHM)


# ==================== REFRESH TOKEN ====================

async def create_refresh_token(
    data: dict,
    db: AsyncSession,
    device_info: str | None = None,
    ip_address: str | None = None
) -> str:
    """Создание Refresh Token"""
    expire = timedelta(days=settings.JWT_REFRESH_DAYS)
    token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    
    refresh_token = RefreshToken(
        user_id=data["user_id"],
        hash_token=token_hash,
        expires_at=datetime.now(timezone.utc) + expire
    )

    db.add(refresh_token)
    await db.commit()
    
    return token

async def get_token_from_cookie_or_header(
    request: Request,
    access_token: Optional[str] = Cookie(None, alias="access_token"),
) -> Optional[str]:
    """
    Достает токен из cookie или заголовка Authorization.
    Приоритет: cookie > header
    """
    # 1. Пробуем взять из cookie
    if access_token:
        return access_token
    
    # 2. Пробуем взять из заголовка Authorization
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header.split(" ")[1]
    
    return None


async def verify_refresh_token(db: AsyncSession, token: str):
    """Проверка Refresh Token"""
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    
    result = await db.execute(
        select(RefreshToken).where(RefreshToken.hash_token == token_hash)
    )
    refresh_token = result.scalar_one_or_none()
    
    if not refresh_token:
        return None
    
    # Проверка истечения
    if refresh_token.expires_at < datetime.now(timezone.utc):
        await db.delete(refresh_token)
        await db.commit()
        return None
    
    # Получение пользователя
    user = await db.get(UserModel, refresh_token.user_id)
    
    if not user or user.is_blocked:
        return None
    
    return user


# ==================== DEPENDENCIES ====================

async def get_current_user(
    request: Request,
    db: AsyncSession = Depends(get_db),
    token: Optional[str] = Depends(get_token_from_cookie_or_header),
) -> UserModel:
    """Получение текущего пользователя из JWT (cookie или header)"""
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось валидировать учетные данные",
        headers={"WWW-Authenticate": "Bearer"}
    )
    
    if token is None:
        raise credentials_exception
    
    try:
        secret_key = settings.JWT_SECRET_KEY or settings.SECRET_KEY
        payload = jwt.decode(token, secret_key, algorithms=[settings.JWT_ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен истёк",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except jwt.InvalidTokenError:
        raise credentials_exception
    
    result = await db.execute(
        select(UserModel).where(
            UserModel.email == email,
            UserModel.is_blocked == False
        )
    )
    user = result.scalar_one_or_none()
    
    if user is None:
        raise credentials_exception
    
    return user


async def get_current_admin(
    current_user: UserModel = Depends(get_current_user)
) -> UserModel:
    """Проверка что текущий пользователь - админ"""
    
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Доступ только для администраторов"
        )
    
    return current_user


async def get_current_psychologist(
    current_user: UserModel = Depends(get_current_user)
) -> UserModel:
    """Проверка что текущий пользователь - психолог"""
    
    if not current_user.is_psychologist:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Доступ только для психологов"
        )
    
    return current_user
