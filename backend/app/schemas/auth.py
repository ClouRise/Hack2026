# app/schemas/auth.py

from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    """Схема для входа в систему"""
    email: EmailStr | str = Field(..., description="Email или логин")
    password: str = Field(..., min_length=1, description="Пароль")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "admin@example.com",
                "password": "admin123"
            }
        }


class LoginResponse(BaseModel):
    """Ответ после успешного входа"""
    access_token: str
    token_type: str = "bearer"