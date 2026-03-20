from plistlib import UID
import uuid
import enum

from app.db.base import Base
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Enum, String




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

    photo_url: Mapped[str] = mapped_column(
        String(255),
        nullable=True
    )