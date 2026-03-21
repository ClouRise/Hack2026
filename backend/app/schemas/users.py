from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

class CreateUser(BaseModel):
    email: EmailStr = Field(max_length=255, description="Почта пользователя(не длинее 2,3)")
    name: str = Field(max_length=255, description="ФИО пользователя")
    phone: Optional[str] = Field(max_length=20, description="Телефон пользователя (до 20 символов), начиная с '+' ", pattern=r'^\+?\d{10,15}$')
    # photo_url: Optional[str] = Field(max_length=500, description="Фотографии")
    # bio: Optional[str] = Field(description="Биография пользователя")

class UpdateExistUser(BaseModel):
    phone: str = Field(max_length=20, description="Телефон пользователя (до 20 символов), начиная с '+' ", pattern=r'^\+?\d{10,15}$')
    photo_url: Optional[str] = Field(max_length=500, description="Фотографии")
    bio: Optional[str] = Field(description="Биография пользователя")

class UserSchema(BaseModel):
    id: int = Field(description="ID пользователя")
    role: str = Field(description="Роль пользователя") 
    email: EmailStr = Field(max_length=250, description="Почта пользователя")
    name: str = Field(max_length=255, description="ФИО пользователя")
    phone: Optional[str] = Field(max_length=20, description="Телефон пользователя, начиная с '+' ", pattern=r'^\+?\d{10,15}$')
    photo_url: Optional[str] = Field(max_length=500, description="Фотография или аватарка")
    bio: Optional[str] = Field(description="Биография")
    is_blocked: bool = Field(description="Статус блокировки пользователя")
    created_at: datetime = Field(description="Время создания учетной записи")
    updated_at: datetime = Field(description="Время обновления данных об учетной записи") #странное поле - убрать при возможности