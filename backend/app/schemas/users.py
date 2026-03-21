import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from app.models.user import UserRole


class CreateUser(BaseModel):
    """Создание пользователя (только для админа)"""
    email: EmailStr = Field(description="Email пользователя")
    name: str = Field(max_length=255, description="ФИО пользователя")
    phone: Optional[str] = Field(
        None,
        max_length=20,
        description="Телефон пользователя",
        pattern=r'^\+?\d{10,15}$'
    )


class UpdateExistUser(BaseModel):
    """Обновление данных пользователя"""
    phone: Optional[str] = Field(
        None,
        max_length=20,
        description="Телефон пользователя",
        pattern=r'^\+?\d{10,15}$'
    )
    photo_url: Optional[str] = Field(None, max_length=500, description="URL фотографии")
    bio: Optional[str] = Field(None, description="Биография пользователя")


class UserSchema(BaseModel):
    """Схема для ответа"""
    id: uuid.UUID = Field(description="ID пользователя")
    role: UserRole = Field(description="Роль пользователя")
    email: EmailStr = Field(description="Email пользователя")
    name: str = Field(description="ФИО пользователя")
    phone: Optional[str] = Field(None, description="Телефон пользователя")
    photo_url: Optional[str] = Field(None, description="URL фотографии")
    bio: Optional[str] = Field(None, description="Биография")
    is_blocked: bool = Field(description="Заблокирован ли пользователь")
    created_at: datetime = Field(description="Дата создания")

    class Config:
        from_attributes = True


class RegisterRequest(BaseModel):
    """Схема для регистрации (для демо)"""
    email: EmailStr
    password: str = Field(min_length=6, description="Пароль")
    name: str = Field(max_length=255)


class CreateUserResponse(BaseModel):
    """Ответ при создании пользователя"""
    user: UserSchema
    temp_password: str = Field(description="Временный пароль для входа")
