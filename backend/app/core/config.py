from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    APP_NAME: str = "FastAPI HACK2026"
    DEBUG: bool = True

    SECRET_KEY: str = ""
    DOCS_USER: str = ""
    DOCS_PASSWORD: str = ""

    SESSION_COOKIE_NAME: str = "session_token"
    SESSION_EXPIRE_SECONDS: int = 60 * 60

    JWT_SECRET_KEY: str = ""
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUT: int = 30

    COOKIE_HTTPONLY: bool = True
    COOKIE_SECURE: bool = False  # True только при HTTPS
    COOKIE_SAMESITE: str = "lax"

    # Database
    POSTGRES_USER: str = "hackathon_user"
    POSTGRES_PASSWORD: str = "hackathon_pass"
    POSTGRES_HOST: str = "localhost"  # имя сервиса из docker-compose
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "hackathon_db"

    @property
    def ASYNC_DATABASE_URL(self) -> str:
        """Async URL для FastAPI и Alembic async"""
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    model_config = SettingsConfigDict(
        env_file=".env", case_sensitive=True, extra="allow"
    )


settings = Settings()
