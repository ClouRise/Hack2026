import uuid
import enum
<<<<<<< HEAD

from ..db.base import Base
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import mapped_column, Mapped
=======
from datetime import datetime, timezone
from typing import Optional, TYPE_CHECKING
from sqlalchemy.orm import mapped_column, Mapped, relationship
>>>>>>> e056c3c17565fad9e39274ce53ffb50018ebc420
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Enum, String, Text, DateTime, Boolean

from app.db.base import Base

if TYPE_CHECKING:
    from .test import Test


class UserRole(str, enum.Enum):
    """РОЛИ ПОЛЬЗОВАТЕЛЯ"""
    ADMIN = "admin"
    PSYCHOLOGIST = "psychologist"


class User(Base):
    """ПОЛЬЗОВАТЕЛИ СИСТЕМЫ"""
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="user_role"),
        nullable=False,
        index=True
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

    phone: Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=True
    )

    photo_url: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True
    )

    bio: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )

    access_until: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
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
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Связи
    tests: Mapped[list["Test"]] = relationship(
        "Test",
        back_populates="psychologist",
        cascade="all, delete-orphan"
    )

    # Методы
    def __repr__(self) -> str:
        return f"<User {self.email} ({self.role.value})>"

    @property
    def is_admin(self) -> bool:
        return self.role == UserRole.ADMIN
    
    @property
    def is_psychologist(self) -> bool:
        return self.role == UserRole.PSYCHOLOGIST
    
    @property
    def has_active_access(self) -> bool:
        """Проверка активности доступа"""
        if self.is_blocked:
            return False
        if self.access_until is None:
            return True
        return datetime.now(timezone.utc) < self.access_until