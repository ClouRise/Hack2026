from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow",
    )

    APP_NAME: str = "FastAPI HACK2026"
    DEBUG: bool = True

    @field_validator("DEBUG", mode="before")
    @classmethod
    def _parse_debug(cls, value):
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            normalized = value.strip().lower()
            if normalized in {"1", "true", "yes", "y", "on", "debug"}:
                return True
            if normalized in {"0", "false", "no", "n", "off", "release", "prod", "production"}:
                return False
        return value

    SECRET_KEY: str = ""
    DOCS_USER: str = ""
    DOCS_PASSWORD: str = ""

    SESSION_COOKIE_NAME: str = "session_token"
    SESSION_EXPIRE_SECONDS: int = 60 * 60

    JWT_SECRET_KEY: str = ""
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_EXPIRE_MINUT: int = 30
    JWT_REFRESH_DAYS: int = 7

    COOKIE_HTTPONLY: bool = True
    COOKIE_SECURE: bool = False  # True только при HTTPS
    COOKIE_SAMESITE: str = "lax"

    # Dev bootstrap
    BOOTSTRAP_ADMIN: bool = True
    BOOTSTRAP_ADMIN_EMAIL: str = "admin@example.com"
    BOOTSTRAP_ADMIN_PASSWORD: str = "admin"

    # Database
    DATABASE_URL: str | None = None
    POSTGRES_USER: str = "h26_user"
    POSTGRES_PASSWORD: str = "123123"
    POSTGRES_HOST: str = "localhost"  # имя сервиса из docker-compose
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "h26_db"

    @property
    def ASYNC_DATABASE_URL(self) -> str:
        """Async URL для FastAPI и Alembic async"""
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


settings = Settings()
