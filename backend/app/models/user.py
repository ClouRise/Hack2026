import uuid
import enum

from app.db.base import Base
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Enum, String, Text, DateTime, Boolean



class UserRole(str, enum.Enum):
    """РОЛИ ПОЛЬЗОВАТЕЛЯ"""
    ADMIN = "ADMIN"
    PSYCHOLOGY = "PSYCHOLOGY"


class User(Base):
    """
    ПОЛЬЗОВАТЕЛИ СИСТЕМЫ
    """
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    phone: Mapped[str] = mapped_column(
        String(12),
        nullable=False
    )

    photo_url: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True
    )

    bio: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )

    access_until: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
        index=True
    )

    is_blocked: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        index=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.now(timezone.utc)
    )

    #CВЯЗЬ

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN
    
    @property
    def is_psychology(self):
        return self.role == UserRole.PSYCHOLOGY
    
    @property
    def has_active_access(self) -> bool:
        """Проверка активности доступа"""
        if self.is_blocked:
            return False
        if self.access_until is None:
            return True
        return datetime.now(timezone.utc) < self.access_until