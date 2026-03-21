
import uuid

from datetime import datetime, timezone
from typing import Optional, TYPE_CHECKING
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy import String, Text, DateTime, Boolean, Integer, ForeignKey

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.user import User


class Token(Base):
    """МОДЕЛЬ ДЛЯ ТОКЕНА"""

    __tablename__ = "refresh_tokens"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    hash_token: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        nullable=False,
        index=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
        comment="Когда истекает токен"
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="refresh_tokens"  # ← МНОЖЕСТВЕННОЕ ЧИСЛО!
    )
    